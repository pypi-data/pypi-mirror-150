#!/usr/bin/env python3
# microst.py - Micro Serial Terminal

from collections import deque
import threading
from typing import Deque, Tuple
import serial
import sys
import curses
import enum
import string
import importlib
import getopt


class SerialPort:
    def __init__(
        self,
        port,
        baudrate,
        bytesize,
        parity,
        stopbits,
        timeout=0.1,
    ):
        """
        Initialize the serial port.
        :param port: The serial port to be used.
        :param baudrate: The baudrate to be used.
        :param bytesize: The bytesize to be used.
        :param parity: The parity to be used.
        :param stopbits: The stopbits to be used.
        :param timeout: The timeout to be used.
        """
        try:
            self._serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                stopbits=stopbits,
                parity=parity,
                timeout=timeout,
            )
        except serial.SerialException:
            # print(f"----- Failed to open {port} -----")
            return None
        # print(f"----- Opened {port} -----")

    def read_string(self) -> str:
        """
        Read a string from the serial port
        """
        return self._serial.read().decode()

    def write(self, data) -> None:
        """
        Writes data to the serial port.
        :param data: The data to be written.
        :return: None
        """
        self._serial.write(data)

    def write_string(self, data: str) -> None:
        """
        Write a string to the serial port
        :param data: The string to be written.
        """
        self._serial.write(data.encode())

    def close(self) -> None:
        """
        Close the serial port
        """
        self._serial.close()

    def is_open(self) -> bool:
        """
        Check if the serial port is open
        """
        return self._serial.is_open


class Console:
    class Modes(enum.Enum):
        """
        Enum for the different modes of the console.
        These modes where inspired by vim.
        """

        NORMAL = 0  # switch between insert and command mode
        INSERT = 1  # interact with the serial port
        COMMAND = 2  # execute commands

    # The initial moe of the console
    # The console starts in insert mode so the user can interrupt the boot sequence if needed
    mode: Modes = Modes.INSERT

    # The text at the bottom of the console
    bottom_text: str = "Press ^] to switch between insert and command mode"

    # The current command
    command: str = ""

    # The previous lines read from the serial port
    serial_history: Deque[str] = deque([""], maxlen=100)

    # A tuple with the last character read from the user and wether it was already printed
    last_ch: Tuple[bytes, bool] = b"", True

    # Should the screen be cleared to add a new line?
    new_line = False

    def __init__(
        self,
        port,
        baudrate,
        bytesize,
        parity,
        stopbits,
    ):
        self.serial = SerialPort(port, baudrate, bytesize, parity, stopbits)
        if self.serial is None:
            print("Failed to open serial port")
            sys.exit(1)

    def set_normal_mode(self, bottom_text: str = "--- Normal Mode ---") -> None:
        """
        Set the console to normal mode.

        In normal mode, the user can switch between insert and command mode.
        The cursor is not visible.

        :param bottom_text: The text to be displayed at the bottom of the screen.
        """
        self.mode = Console.Modes.NORMAL
        self.bottom_text = bottom_text
        curses.curs_set(0)

    def read_serial(self) -> None:
        """
        Reads data from the serial port and adds it to the history.
        """
        s_read = self.serial.read_string()
        if s_read:
            r = s_read.split("\n")

            # Adds any dangling strings to the previous line
            self.serial_history[-1] += r[0]

            # If a new line was read, the screen needs to be cleared to add space for it
            self.new_line = len(r) > 1

            for line in r[1:]:
                self.serial_history.append(line)

    def draw(self, stdscr) -> None:
        """
        Draws the console.

        This function can probably be optimized, I'm pretty new to curses.

        :param stdscr: The screen to be drawn on.
        """

        ROWS, COLS = stdscr.getmaxyx()

        # We are interested in the last writable row
        ROWS -= 1

        if self.new_line:
            stdscr.clear()

        start = max(0, len(self.serial_history) - ROWS)
        for i in range(start, len(self.serial_history)):
            stdscr.addstr(start + i, 0, self.serial_history[i])

        y, x = stdscr.getyx()

        if self.new_line or self.last_ch[1]:
            ch = self.last_ch[0]
            self.last_ch = ch, False
            ch = ch.decode()

            # Draw the bottom text
            if self.mode == Console.Modes.COMMAND:
                stdscr.move(ROWS, 0)
                stdscr.clrtoeol()
                stdscr.addstr(ROWS, 0, self.command)
            else:
                # This can probably be optimized away
                stdscr.move(ROWS, 0)
                stdscr.clrtoeol()
                stdscr.addstr(ROWS, 0, self.bottom_text)

            # Prints the last input character if it is printable
            if ch in string.printable and ch != "\n":
                stdscr.addstr(ROWS, COLS - 5, ch)

        # Move the cursor
        if self.mode == Console.Modes.NORMAL:
            # In normal mode, the cursor is not visible so we don't move it
            pass
        elif self.mode == Console.Modes.COMMAND:
            # In command mode, the cursor is at the end of the command
            stdscr.move(ROWS, len(self.command))
        else:
            stdscr.move(y, x)

        if self.new_line:
            self.new_line = False

        stdscr.refresh()

    def run(self, stdscr) -> int:
        """
        Runs the console.

        This function is the main loop of the console.
        It needs to be refactored.

        :param stdscr: The screen to be drawn on.
        :return: The exit code.
        """
        stdscr.clear()
        stdscr.refresh()

        serial_queue = deque()

        def read_user_input() -> None:
            """
            Reads user input and adds it to the appropriate queue.
            """

            while self.serial.is_open():
                try:
                    ch: bytes = stdscr.getch().to_bytes(1, "little")
                except OverflowError:
                    # This happens when the user presses arrow keys for example
                    # TODO: Find a better way to handle this
                    continue

                self.last_ch = ch, True

                if self.mode == Console.Modes.NORMAL:
                    if ch == b"i":  # Switch to insert mode
                        self.mode = Console.Modes.INSERT
                        self.bottom_text = "--- INSERT ---"
                        curses.curs_set(1)  # Sets the cursor to visible
                        continue

                    elif ch == b":":  # Switch to command mode
                        self.mode = Console.Modes.COMMAND
                        self.command = ":"
                        curses.curs_set(1)
                        continue

                elif self.mode == Console.Modes.COMMAND:
                    if ch in [b"\x1b", b"\x1d"]:  # Escape and go back to command mode
                        self.set_normal_mode()
                        continue

                    elif ch == b"\n":  # Enter
                        # If the command is empty, we don't do anything
                        if not self.command or self.command[0] != ":":
                            continue

                        if self.command == ":q" or self.command == ":quit":
                            return 0
                        elif ":send " == self.command[:6]:
                            try:
                                filename = self.command[6:]
                                with open(filename, "rb") as f:
                                    self.serial.write(f.read())
                                self.set_normal_mode("SENT")
                            except Exception as e:
                                print(
                                    f"Error while attempting to send {self.command[6:]}"
                                )
                                print(e)
                                self.set_normal_mode("FAILED TO SEND FILE")
                            continue
                        elif ":exec " == self.command[:6]:
                            try:
                                [filename, *args] = self.command[6:].split(" ")

                                if filename[:-3] == ".py":
                                    filename = filename[:-3]

                                fun_name: str = "main"
                                if args:
                                    fun_name = args[0]
                                    args = args[1:]

                                lib = importlib.import_module(filename)

                                fun = getattr(lib, fun_name)

                                res = str(fun(self.serial._serial, *args))

                                self.set_normal_mode(
                                    f"EXECUTED {self.command[6:]} => {res}"
                                )

                            except Exception as e:
                                print(
                                    f"Error while attempting to execute {self.command[6:]}"
                                )
                                print(e)
                                self.set_normal_mode("FAILED TO EXECUTE FILE")
                            continue
                        else:
                            self.set_normal_mode("UNKNOWN COMMAND")
                            continue

                    elif ch in [b"\x08", b"\x7f"]:  # Backspace and Delete
                        if len(self.command) > 0:
                            self.command = self.command[:-1]
                        continue

                    # TODO: Add support for tab

                    self.command += ch.decode()

                elif self.mode == Console.Modes.INSERT:
                    if ch == b"\x1d":  # ^] and go back to command mode
                        self.set_normal_mode()
                        continue

                    serial_queue.append(ch)

        thread = threading.Thread(target=read_user_input)

        thread.start()

        try:
            while thread.is_alive():
                # Sends the user inputs through the serial port
                serial_len = len(serial_queue)
                if serial_len > 0:
                    self.serial.write(
                        b"".join(serial_queue.popleft() for _ in range(serial_len))
                    )

                # Reads the serial port and writes it to the console
                self.read_serial()

                # draw the console
                self.draw(stdscr)
        finally:
            self.serial.close()

        return 0


help_str = """Usage: microst -p port [-b baudrate] [-c bytesize] [-s stopbits] [-P parity]

Arguments:
    -h, --help:     Show this help message and exit

    -p, --port:     The serial port to connect to.

    -b, --baudrate: The baudrate to use. (Default: 9600)
        Available baudrates:
            300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600,
            115200, 128000, 256000

    -c, --bytesize: The bytesize to use. (Default: 8)

    -s, --stopbits: The stopbits to use. (Default: 1)
        Available values: 1, 2

    -P, --parity:   The parity to use. (Default: N)
        Available options:
            E: Even parity
            O: Odd parity
            N: No parity
            M: Mark parity
            S: Space parity
"""


def main():
    port = None
    baudrate = 9600
    bytesize = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "p:b:c:s:P:h",
            ["port=", "baudrate=", "bytesize=", "stopbits=", "parity="],
        )
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = arg
        elif opt in ("-b", "--baudrate"):
            baudrate = int(arg)
            if baudrate not in [
                300,
                600,
                1200,
                2400,
                4800,
                9600,
                14400,
                19200,
                28800,
                38400,
                57600,
                115200,
                128000,
                256000,
            ]:
                raise ValueError(f"Invalid baudrate {arg}")
        elif opt in ("-c", "--bytesize"):
            bytesize = arg
        elif opt in ("-s", "--stopbits"):
            if arg == "1":
                stopbits = serial.STOPBITS_ONE
            elif arg == "2":
                stopbits = serial.STOPBITS_TWO
            else:
                raise ValueError(f"Invalid stopbits {arg}")
        elif opt in ("-P", "--parity"):
            if arg == "E":
                parity = serial.PARITY_EVEN
            elif arg == "O":
                parity = serial.PARITY_ODD
            elif arg == "N":
                parity = serial.PARITY_NONE
            elif arg == "M":
                parity = serial.PARITY_MARK
            elif arg == "S":
                parity = serial.PARITY_SPACE
            else:
                raise ValueError(f"Unknown parity: {arg}")
        elif opt in ("-h", "--help"):
            print(help_str)
            sys.exit()

    if not port:
        print(help_str)
        sys.exit(2)

    console = Console(port, baudrate, bytesize, parity, stopbits)
    curses.wrapper(console.run)

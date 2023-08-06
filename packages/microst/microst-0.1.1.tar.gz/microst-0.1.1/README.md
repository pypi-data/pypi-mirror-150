# μ Serial Terminal

A micro serial terminal written in Python.

## Usage

```plaintext
Usage: microst -p port [-b baudrate] [-c bytesize] [-s stopbits] [-P parity]

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
```

## Features

I needed a serial terminal that allowed me to send files and in general more flexibility than a standard terminal.

This terminal therefore has VI style modes, which are:

### 💬 Insert mode

> ⚠ It is the default mode.

Insert mode is used to communicate with the serial port, it can be accessed by pressing `i` from normal mode.

### 🔀 Normal mode

Normal mode is used to switch between modes.

> ⚠ It can be accessed by pressing `<ctrl> ]` rather than `<esc>`. That way, `<esc>` can be sent to the serial port.

### ⚡ Command mode

Command mode is activated by pressing the `:` key from normal mode. Currently, there are 3 commands:

#### `:q`

Quit the terminal.

#### `:send <filename>`

Send the file `<filename>` to the connected device.

#### `exec <filename> [<function name> <arguments>]`

Executes the function `<function name>` (or `main` if not specified) with `Serial` object and the arguments `<arguments>`.

For example, with the following file:

```python
# my_script.py

import serial


def send_file(s: serial.Serial, filename: str):
    with open(filename, "rb") as f:
        s.write(f.read())
    return 1
```

executing `:exec my_script send_file foo.bin` will send the file `foo.bin` to the connected device.

(we could also have used `:send foo.bin`)

## Installation

μst can be installed with pip:

```plaintext
$ pip install microst
```

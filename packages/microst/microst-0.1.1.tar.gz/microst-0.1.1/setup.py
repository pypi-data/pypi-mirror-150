# -*- coding: utf-8 -*-

from setuptools import setup


with open("Readme.md", "r", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="microst",
    version="0.1.1",
    description="micro serial terminal",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jack Royer",
    author_email="jack.royer.23@gmail.com",
    license="MIT",
    url="https://github.com/Garfield1002/microst",
    entry_points={
        "console_scripts": ["microst=microst.microst:main"],
    },
    packages=["microst"],
    include_package_data=False,
    install_requires=["pyserial"],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["serial", "terminal"],
)

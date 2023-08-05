#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="cli-tictactoe",
    version="1.0.4",
    description="A module to simulate a TicTacToe game",
    long_description=readme(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    author="Hugo Campos",
    author_email="hugohvlcampos96@gmail.com",
    url="https://github.com/HugoValim/TicTacToe",
    install_requires=[],
    packages=find_packages(exclude=["test", "test.*"]),
    entry_points={"console_scripts": ["ttt=cli_tictactoe.scripts.run:run_game"]},
)

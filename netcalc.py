#! /usr/bin/env python

# Netcalc - advanced network calculator and address planning helper
# Copyright (C) 2016 Israel G. Lugo
#
# This file is part of netcalc.
#
# Netcalc is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Netcalc is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with netcalc. If not, see <http://www.gnu.org/licenses/>.
#
# For suggestions, feedback or bug reports: israel.lugo@lugosys.com


"""Main program file."""


# Be compatible with Python 3
from __future__ import print_function

import os
import sys
import argparse

import commands


__version__ = "0.1.0"


__all__ = [ 'main' ]



def workaround_argparse_bug(subparsers):
    """Work around argparse bug on Python 3.3 and above.

    Subcommands should be mandatory, and they are treated as optional.
    Impact is that argparse will not give an error if the user runs us
    without any arguments, therefore we break with an exception when trying
    to call args.func().

    See http://bugs.python.org/issue9253

    """
    if sys.version_info >= (3, 3):
        # take advantage of the fact that subparsers is actually an Action,
        # and directly set its 'required' field
        subparsers.required = True


def parse_args():
    """Parse command-line arguments.

    Returns a populated namespace with all arguments and their values.

    """
    parser = argparse.ArgumentParser(
            description="Advanced network calculator and address planning helper.")

    subparsers = parser.add_subparsers(help="available commands",
            dest="command", metavar="COMMAND")
    workaround_argparse_bug(subparsers)

    for cls in commands.commands:
        cls(subparsers)

    args = parser.parse_args()

    return args


def main():
    """Main program function."""

    prog_name = os.path.basename(sys.argv[0])
    args = parse_args()

    try:
        args.func(args)
    except argparse.ArgumentTypeError as e:
        sys.stderr.write("%s %s: error: %s\n" % (prog_name, args.command, str(e)))
        sys.exit(1)


if __name__ == '__main__':
    main()

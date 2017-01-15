#! /usr/bin/env python

# NetCalc - advanced network calculator and address planning helper
# Copyright (C) 2016, 2017 Israel G. Lugo
#
# This file is part of NetCalc.
#
# NetCalc is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# NetCalc is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with NetCalc. If not, see <http://www.gnu.org/licenses/>.
#
# For suggestions, feedback or bug reports: israel.lugo@lugosys.com


"""Main CLI user interface."""


# Be compatible with Python 3
from __future__ import print_function

import os
import sys
import argparse

import netcalc.command as command
from netcalc.version import __version__


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
    fromfile_prefix_chars='@'
    parser = argparse.ArgumentParser(
            fromfile_prefix_chars=fromfile_prefix_chars,
            description="Advanced network calculator and address planning helper.",
            epilog="Arguments can be expanded in-place from the contents of a file, by referencing the file with a '%s'."
                    % fromfile_prefix_chars)

    # This doesn't show license information, a la GNU. Would be nice.
    # Create a custom Action that prints what we want and exits?  Can't
    # place everything in "version" string, because the default formatter
    # wraps everything.
    parser.add_argument('-V', '--version', action='version', version="NetCalc %s" % __version__)

    subparsers = parser.add_subparsers(help="available commands",
            dest="command", metavar="COMMAND")
    workaround_argparse_bug(subparsers)

    for cls in command.commands:
        cls(subparsers, parser)

    args = parser.parse_args()

    return args


def main():
    """Main program function."""

    prog_name = os.path.basename(sys.argv[0])
    args = parse_args()

    try:
        args.func(args)
    except command.CommandError as e:
        sys.stderr.write("%s %s: error: %s\n" % (prog_name, args.command, str(e)))
        sys.exit(1)


if __name__ == '__main__':
    main()


# vim: set expandtab smarttab shiftwidth=4 softtabstop=4 tw=75 :

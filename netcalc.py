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


# Be compatible with Python 3
from __future__ import print_function

import sys
import argparse

import netaddr


__version__ = "0.1.0"


__all__ = [ 'main' ]



def do_add(args):
    """Add networks together, merging as much as possible."""

    merged = netaddr.cidr_merge(args.networks)

    for i in merged:
        print(i)


def network_address(string):
    """Convert a string to a network address, if possible.

    Returns a netaddr.IPNetwork instance. Raises netaddr.ArgumentTypeError
    if string is not a valid network.

    """
    try:
        network = netaddr.IPNetwork(string)
    except netaddr.AddrFormatError as e:
        raise argparse.ArgumentTypeError("invalid network address '%s'" % string)

    return network


def parse_args():
    """Parse command-line arguments.

    Returns a populated namespace with all arguments and their values.

    """
    parser = argparse.ArgumentParser(
            description="Advanced network calculator and address planning helper.")

    subparsers = parser.add_subparsers(help="available commands", metavar="COMMAND")

    parser_add = subparsers.add_parser('add',
                                       help="add networks, merging as much as possible")
    parser_add.add_argument('networks', metavar='NETWORK', type=network_address,
                            nargs='+', help="a network address")
    parser_add.set_defaults(func=do_add)

    args = parser.parse_args()

    return args


def main():
    """Main program function."""

    args = parse_args()

    args.func(args)


if __name__ == '__main__':
    main()

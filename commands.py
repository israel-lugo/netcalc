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


"""Command implementations."""


# Be compatible with Python 3
from __future__ import print_function

import netaddr


__all__ = [ 'command_registrators' ]


def add_parser_compat(subparsers, *args, **kwargs):
    """Add a parser to an argparse subparsers object.

    Adds the parser in a Python 2/3 compatible manner. In particular,
    Python 2 doesn't support the aliases keyword argument. Tries to use
    this option it if possible, omit it otherwise.

    """
    try:
        subparser = subparsers.add_parser(*args, **kwargs)

    except TypeError as e:
        # Failed. We're probably running on Python 2.x, which doesn't
        # support the "aliases" keyword argument. Try again.
        kwargs2 = kwargs.copy()
        try:
            del kwargs2['aliases']
        except KeyError:
            # there is no "aliases", original error was something else
            raise e

        subparser = subparsers.add_parser(*args, **kwargs2)

    return subparser


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


def register_add(subparsers):
    """Register the add command on an argparse subparsers object.

    Returns the subparser and the action function for this command.

    """
    subparser = add_parser_compat(subparsers, 'add',
        help="add networks, merging as much as possible", aliases=["merge"])

    subparser.add_argument('networks', metavar='NETWORK', type=network_address,
        nargs='+', help="a network address")

    return subparser, do_add


def do_add(args):
    """Add networks together, merging as much as possible."""

    merged = netaddr.cidr_merge(args.networks)

    for i in merged:
        print(i)


command_registrators = [
    register_add,
]
"""List of command registrator functions."""

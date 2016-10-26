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

import sys

import netaddr


__all__ = [ 'command_registrators' ]


def add_parser_compat(subparsers, *args, **kwargs):
    """Add a parser to an argparse subparsers object.

    Adds the parser in a Python 2/3 compatible manner. In particular,
    Python 2's argparse doesn't support the aliases keyword argument to
    add_parser(). Uses this option if possible, omits it otherwise.

    """
    if sys.version_info >= (3, 2):
        kwargs2 = kwargs
    else:
        # Python 2.x's argparse doesn't support the "aliases" keyword
        # argument. Remove it if present.
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
    subparser = add_parser_compat(subparsers, 'add', aliases=["merge"],
            help="add networks, merging as much as possible")

    subparser.add_argument('networks', metavar='NETWORK',
            type=network_address, nargs='+', help="a network address")

    return subparser, do_add


def do_add(args):
    """Add networks together, merging as much as possible."""

    merged = netaddr.cidr_merge(args.networks)

    for i in merged:
        print(i)



def register_subtract(subparsers):
    """Register the sub command on an argparse subparsers object.

    Returns the subparser and the action function for this command.

    """
    subparser = add_parser_compat(subparsers, 'subtract', aliases=["exclude"],
            help="subtract a network from another, dividing as necessary")

    subparser.add_argument('container', metavar='CONTAINER',
            type=network_address, help="container network address")

    subparser.add_argument('network', metavar='REMOVE', type=network_address,
            help="network address to remove")

    return subparser, do_subtract


def do_subtract(args):
    """Subtract a network from another, dividing as necessary."""

    remainder = netaddr.cidr_exclude(args.container, args.network)

    for i in remainder:
        print(i)



command_registrators = [
    register_add, register_subtract,
]
"""List of command registrator functions."""

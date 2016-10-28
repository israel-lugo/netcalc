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
import itertools
import argparse

import netaddr



def _network_address(string):
    """Convert a string to a network address, if possible.

    Returns a netaddr.IPNetwork instance. Raises netaddr.ArgumentTypeError
    if string is not a valid network.

    """
    try:
        network = netaddr.IPNetwork(string)
    except netaddr.AddrFormatError as e:
        raise argparse.ArgumentTypeError("invalid network address '%s'" % string)

    return network



class Command:
    """Base class for all commands.

    This class MUST be subclassed. Subclasses MUST define the following methods:

        __init__(self, subparsers)

        func(self, args)

    """
    def __init__(self, subparsers):
        """Initialize and register on an argparse subparsers object.

        Registers Command.func() as an action for the suparser.

        """

        raise NotImplementedError("BUG: Command.__init__() must be overriden")

    def func(self, args):
        """Execute the command, with a list of arguments.

        This must be overriden. It is meant to be called as an action
        function, by the main arg parser.

        """
        raise NotImplementedError("BUG: Command.func() must be overriden")

    @staticmethod
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

    @staticmethod
    def warn(msg):
        """Print a warning message to stderr."""
        sys.stderr.write("warning: %s\n" % msg)



class AddCommand(Command):
    def __init__(self, subparsers):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'add', aliases=["merge"],
                help="add networks, merging as much as possible")

        subparser.add_argument('networks', metavar='NETWORK',
                type=_network_address, nargs='+', help="a network address")

        subparser.set_defaults(func=self.func)

    def func(self, args):
        """Add networks together, merging as much as possible."""

        merged = netaddr.cidr_merge(args.networks)

        for i in merged:
            print(i)


class SubtractCommand(Command):
    def __init__(self, subparsers):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'sub', aliases=["remove"],
                help="subtract a network from another, splitting as necessary")

        subparser.add_argument('container', metavar='CONTAINER',
                type=_network_address, help="container network address")

        subparser.add_argument('network', metavar='REMOVE', type=_network_address,
                help="network address to remove")

        subparser.set_defaults(func=self.func)

    def func(self, args):
        """Subtract a network from another, dividing as necessary."""

        remainder = netaddr.cidr_exclude(args.container, args.network)

        for i in remainder:
            print(i)


class ExprCommand(Command):
    def __init__(self, subparsers):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'expr', aliases=["math"],
                help="add and subtract networks using an expression")

        subparser.add_argument('expression', metavar='EXPRESSION',
                nargs='+', help="an expression like NETWORK + NETWORK - NETWORK")

        subparser.set_defaults(func=self.func)

    def func(self, args):
        """Evaluate an expression of adding and subtracting networks."""

        expr = args.expression
        accum = [_network_address(expr.pop(0))]

        while len(expr) >= 2:
            operator = expr.pop(0)
            # right-hand side of the expression
            rhs = _network_address(expr.pop(0))

            if operator in ("+", "add", "merge"):
                # add (merge) in a new network
                accum = netaddr.cidr_merge(accum + [rhs])
            elif operator in ("-", "sub", "remove"):
                # subtract (remove) a network

                # for each network in accum, remove the RHS from it, then
                # chain everything into a single flat generator sequence
                # (RHS may be partially contained in more than one accum
                # network)
                minus_rhs = itertools.chain.from_iterable(
                                netaddr.cidr_exclude(network, rhs)
                                for network in accum
                            )
                accum = netaddr.cidr_merge(minus_rhs)

        if expr:
            self.warn("ignoring extra argument '%s'" % ' '.join(expr))

        for i in accum:
            print(i)



commands = [
    AddCommand, SubtractCommand, ExprCommand
]
"""List of command classes."""

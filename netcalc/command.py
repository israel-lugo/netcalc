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


"""Command implementations."""


# Be compatible with Python 3
from __future__ import print_function

import sys
import itertools
import argparse

import netaddr



class CommandError(Exception):
    """Base class for errors while executing a command."""
    def __init__(self, msg):
        """Initialize and store a message argument."""
        self.msg = msg

    def __str__(self):
        """Convert to string."""
        return self.msg


class CommandParseError(CommandError, argparse.ArgumentTypeError):
    """Error while parsing a command.

    Apart from being a CommandError, this is also a subclass of
    argparse.ArgumentTypeError. This is so that argparse.parse_args()
    recognizes this as an argument error, and handles it as such (by
    printing an error and exiting).

    """
    pass


def _network_address(string):
    """Convert a string to a network address, if possible.

    Returns a netaddr.IPNetwork instance. Raises CommandParseError if
    string is not a valid network. This is meant to be caught by the
    argparse.arg_parse(), to print an error and exit.

    """
    try:
        network = netaddr.IPNetwork(string)
    except netaddr.AddrFormatError:
        raise CommandParseError("invalid network address '%s'" % string)

    return network



class Command(object):
    """Base class for all commands.

    This class MUST be subclassed. Subclasses MUST define the following methods:

        __init__(self, subparsers, parser)

        func(self, args)

    """
    def __init__(self, subparsers, parser):
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
            del kwargs2['aliases']

        subparser = subparsers.add_parser(*args, **kwargs2)

        return subparser

    @staticmethod
    def warn(msg):
        """Print a warning message to stderr."""
        sys.stderr.write("warning: %s\n" % msg)



class AddCommand(Command):
    """Add networks, aggregating as much as possible.

    Arguments:
        NETWORK [NETWORK ...]

    Example:
      >>> parser = argparse.ArgumentParser()
      >>> subparsers = parser.add_subparsers()
      >>> add = AddCommand(subparsers, parser)
      >>> args = parser.parse_args("add 198.18.0.0/24 198.18.1.0/24 10.1/16 10/16".split())
      >>> args.func(args)
      10.0.0.0/15
      198.18.0.0/23

    """
    def __init__(self, subparsers, parser):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'add', aliases=["aggregate", "merge"],
                help="add networks, aggregating as much as possible",
                epilog=parser.epilog)

        subparser.add_argument('networks', metavar='NETWORK',
                type=_network_address, nargs='+', help="a network address")

        subparser.set_defaults(func=self.func)

    @staticmethod
    def _get_networks(args):
        """Get the IPNetwork objects to work on.

        This method is useful for subclasses to redefine, to specify a
        different way of getting the networks.

        """
        return args.networks

    def func(self, args):
        """Add networks together, aggregating as much as possible.

        Uses self._get_networks() to get the networks. Subclasses may
        want to redefine that method.

        """
        networks = self._get_networks(args)
        merged = netaddr.cidr_merge(networks)

        for i in merged:
            print(i)


class AddFileCommand(AddCommand):
    """AddCommand variant that reads the networks from a file.

    Arguments:
        FILE

    Example:
      >>> parser = argparse.ArgumentParser()
      >>> subparsers = parser.add_subparsers()
      >>> addfile = AddFileCommand(subparsers, parser)
      >>> args = parser.parse_args("add-file /path/to/file.txt".split())
      >>> args.func(args)
      10.0.0.0/15
      198.18.0.0/23

    """
    def __init__(self, subparsers, parser):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'add-file',
                aliases=["aggregate-file", "merge-file"],
                help="add networks from a file, aggregating as much as possible",
                epilog=parser.epilog)

        subparser.add_argument('file_', metavar='FILE',
                type=argparse.FileType('rt'),
                help="file from which to read the networks")

        subparser.set_defaults(func=self.func)

    @staticmethod
    def _get_networks(args):
        """Get the IPNetwork objects to work on."""

        # TODO: Support other filetypes, with some kind of --format option
        # from our argument parsing

        for line in args.file_:
            stripped = line.strip()
            if stripped:
                yield _network_address(stripped)


class SubtractCommand(Command):
    """Subtract a network from another, splitting as necessary.

    Arguments:
        CONTAINER REMOVE

    Example:
      >>> parser = argparse.ArgumentParser()
      >>> subparsers = parser.add_subparsers()
      >>> sub = SubCommand(subparsers, parser)
      >>> args = parser.parse_args("sub 192.0.2.0/24 192.0.2.0/28".split())
      >>> args.func(args)
      192.0.2.16/28
      192.0.2.32/27
      192.0.2.64/26
      192.0.2.128/25

    """
    def __init__(self, subparsers, parser):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'sub', aliases=["remove"],
                help="subtract a network from another, splitting as necessary",
                epilog=parser.epilog)

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


class SplitCommand(Command):
    """Split a network into subnets of a certain length.

    Arguments:
        NETWORK LENGTH

    Example:
      >>> parser = argparse.ArgumentParser()
      >>> subparsers = parser.add_subparsers()
      >>> split = SplitCommand(subparsers, parser)
      >>> args = parser.parse_args("split 198.18.64.0/18 20".split())
      >>> args.func(args)
      198.18.64.0/20
      198.18.80.0/20
      198.18.96.0/20
      198.18.112.0/20

    """
    def __init__(self, subparsers, parser):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'split',
                aliases=["divide"],
                help="split a network into subnets of a certain length",
                epilog=parser.epilog)

        subparser.add_argument('network', metavar='NETWORK',
                type=_network_address, help="a network address")

        subparser.add_argument('length', metavar='LENGTH', type=int,
                help="prefix length")

        subparser.add_argument('maxlength', nargs='?', metavar='MAXLENGTH',
                type=int, default=None,
                help="maximum length, enables hierarchical splitting")

        subparser.set_defaults(func=self.func)

    def func(self, args):
        """Split a network into subnets of a certain length."""

        ipnetwork = netaddr.IPNetwork(args.network)

        if ipnetwork.version == 4:
            maxlen = 32
        elif ipnetwork.version == 6:
            maxlen = 128
        else:
            raise RuntimeError("unexpected IP version")

        length = args.length
        if not ipnetwork.prefixlen <= length <= maxlen:
            raise CommandParseError("invalid prefix length, must be between %d and %d"
                    % (ipnetwork.prefixlen, maxlen))

        maxlength = args.maxlength
        if maxlength is None:
            maxlength = length
        elif not length <= maxlength <= maxlen:
            raise CommandParseError("invalid max length, must be between %d and %d"
                    % (length, maxlen))

        # This is a non-recursive Depth-First Search over the tree of
        # networks, using a list as accumulator. The accumulator contains
        # tuples (depth, subnets) for a given prefix length. We can't
        # iterate over the accumulator, because we're changing it as we go.
        maxdepth = maxlength - length
        depth = 0
        accum = [(0, ipnetwork.subnet(length))]
        while accum:
            depth, subnets = accum[-1]

            fmt = '  ' * depth + '%s'

            if depth < maxdepth:
                net = next(subnets, None)
                if net is None:
                    # generator was empty; remove and move on
                    del accum[-1]
                    continue
                print(fmt % net)

                # append our children to the accumulator
                depth += 1
                accum.append((depth, net.subnet(length+depth)))

            elif depth == maxdepth:
                # don't expand, just print everything at this level
                for net in subnets:
                    print(fmt % net)
                # remove empty generator
                del accum[-1]



class ExprCommand(Command):
    """Execute an arbitrary arithmetic expression on networks.

    Arguments:
        NETWORK (+|-) NETWORK [(+|-) NETWORK ...]
        NETWORK (add|sub) NETWORK [(add|sub) NETWORK ...]

    Possible operators are + or - (add or sub), with left to right
    associativity.

    Example:
      >>> parser = argparse.ArgumentParser()
      >>> subparsers = parser.add_subparsers()
      >>> expr = ExprCommand(subparsers, parser)
      >>> args = parser.parse_args("expr 10.16/13 - 10.20/14 + 10/12".split())
      >>> args.func(args)
      10.0.0.0/12
      10.16.0.0/14

    """
    def __init__(self, subparsers, parser):
        """Initialize and register on an argparse subparsers object."""

        subparser = self.add_parser_compat(subparsers, 'expr', aliases=["math"],
                help="add and subtract networks using an expression",
                epilog=parser.epilog)

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
            else:
                raise CommandParseError("invalid operator '%s'" % operator)

        if expr:
            self.warn("ignoring extra argument '%s'" % ' '.join(expr))

        for i in accum:
            print(i)



commands = [
    AddCommand, AddFileCommand, SubtractCommand, SplitCommand, ExprCommand
]
"""List of command classes."""


# vim: set expandtab smarttab shiftwidth=4 softtabstop=4 tw=75 :

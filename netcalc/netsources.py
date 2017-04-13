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


"""Sources of IP networks."""


# Be compatible with Python 3
from __future__ import print_function

import re
import netaddr



def _network_or_none(string):
    """Convert a string to a network address, or return None.

    Returns a netaddr.IPNetwork instance if the string is a valid network.
    Returns None otherwise.

    """
    try:
        network = netaddr.IPNetwork(string)
    except netaddr.AddrFormatError:
        network = None

    return network


class NetworkSource(object):
    """Base class for all network sources."""

    def __iter__(self):
        """Get an iterator for the networks.

        This must be overriden.

        """
        raise NotImplementedError("BUG: NetworkSource.__iter__() must be overriden")


class NetworkSourceIdentity(NetworkSource):
    """Source networks from a preexisting sequence of IPNetwork.

    This is meant as a noop network source, to be used when there is
    already a list but there is still a need to be signature-compatible
    with other things that require a network source.

    """

    def __init__(self, networks):
        self._networks = networks

    def __iter__(self):
        """Iterate over the networks."""
        return iter(self._networks)


class NetworkSourceFile(NetworkSource):
    """Source networks from a file, one per line."""

    def __init__(self, file_):
        self._file = file_

    def __iter__(self):
        """Iterate over the networks."""
        for line in self._file:
            stripped = line.strip()
            if stripped:
                yield netaddr.IPNetwork(stripped)

class NetworkSourceFileDetect(NetworkSourceFile):
    """Source networks from a file, autodetect."""

    _ipv4_like = r"(?:(?<!\.)\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?\b(?!\.))"

    # TODO: Create a regexp for IPv6-like strings, and combine them

    _re_network_like = re.compile(_ipv4_like)

    def __iter__(self):
        """Iterate over the networks."""
        for line in self._file:
            # look for stuff that sort of looks like it might be a network
            maybe_networks = self._re_network_like.finditer(line)

            # check the possible networks and yield valid ones
            for maybe_network in maybe_networks:
                network = _network_or_none(network.group(0))

                if network is not None:
                    yield network


# vim: set expandtab smarttab shiftwidth=4 softtabstop=4 tw=75 :


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


"""Advanced network calculator and address planning helper.

NetCalc is a tool made by network admins, for network admins. It supports
adding (aggregating) networks, subtracting a network from a larger network,
doing addition and subtraction of multiple networks at once, and more
functionality is to come in future releases.

NetCalc supports both IPv4 and IPv6, and works very efficiently even with very
large networks. It uses the excellent netaddr library for the core address
manipulation.

This program requires either Python 3 (recommended) or Python 2.

"""


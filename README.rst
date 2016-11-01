NetCalc
=======

|license| |Codacy Badge|

Advanced network calculator and address planning helper.

NetCalc is a tool made by network admins, for network admins. It supports
adding (aggregating) networks, subtracting a network from a larger network,
doing addition and subtraction of multiple networks at once, and more
functionality is to come in future releases.

NetCalc supports both IPv4 and IPv6, and works very efficiently even with very
large networks. It uses the excellent netaddr_ library for the core address
manipulation.

This program requires either Python 3 (recommended) or Python 2.


Usage
-----

Using NetCalc is quite simple. There are three main commands:

add
  Add networks, aggregating as much as possible. ::

    $ netcalc add 198.18.0.0/24 198.18.1.0/24 10.1/16 10/16
    10.0.0.0/15
    198.18.0.0/23

sub
  Subtract a network from another, splitting as necessary. ::

    $ netcalc sub 192.0.2.0/24 192.0.2.0/28
    192.0.2.16/28
    192.0.2.32/27
    192.0.2.64/26
    192.0.2.128/25

expr
  Add and subtract networks using an arbitrarily long mathematical expression. ::

    $ netcalc expr 2001:db8::/34 - 2001:db8::/38 + 2001:db8:100::/41
    2001:db8:100::/41
    2001:db8:400::/38
    2001:db8:800::/37
    2001:db8:1000::/36
    2001:db8:2000::/35


Future plans
------------

Future plans for NetCalc include, in no particular order:

- new command for static information (netmask/bitmask, IP range)
- new command for WHOIS queries
- new command for splitting a network into smaller networks by prefix length
- ability to specify network arguments through a file
- ???

Suggestions are quite welcome :)


Contact
-------

NetCalc is developed by Israel G. Lugo <israel.lugo@lugosys.com>. Main
repository for cloning, submitting issues and/or forking is at
https://github.com/israel-lugo/netcalc


License
-------

Copyright (C) 2016 Israel G. Lugo <israel.lugo@lugosys.com>

NetCalc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

NetCalc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with NetCalc.  If not, see <http://www.gnu.org/licenses/>.


.. |license| image:: https://img.shields.io/badge/license-GPLv3+-blue.svg?maxAge=2592000
   :target: LICENSE
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/4479f8bd8ddd4ba58c09867bf97133cd
   :target: https://www.codacy.com/app/israel-lugo/netcalc
.. _netaddr: https://github.com/drkjam/netaddr


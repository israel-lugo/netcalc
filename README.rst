NetCalc
=======

|license| |PyPi version| |PyPi pyversion| |Codacy Badge|

Advanced network calculator and address planning helper.

NetCalc is a tool made by network admins, for network admins. It supports
adding (aggregating) networks, subtracting a network from a larger network,
doing addition and subtraction of multiple networks at once, and more
functionality is to come in future releases.

NetCalc supports both IPv4 and IPv6, and works very efficiently even with very
large networks. It uses the excellent netaddr_ library for the core address
manipulation.

This program requires either Python 3 (recommended) or Python 2.

.. contents::


Usage
-----

Using NetCalc is quite simple. All functionality is split into commands, each
of which receive their own set of specific arguments.

add command
...........

Add networks, aggregating as much as possible. ::

  $ netcalc add 198.18.0.0/24 198.18.1.0/24 10.1/16 10/16
  10.0.0.0/15
  198.18.0.0/23

This command can be very useful e.g. for calculating a minimal set of prefixes
to announce with BGP.

Another real-life example would be comparing the routing tables from two
separate routers (each with prefixes broken up in different ways), to see if
they are equivalent (both cover the same networks). If the aggregate from one
router matches the aggregate from the other, then they are indeed equivalent.

add-file command
................

Add networks from a file, aggregating as much as possible.

This is a variant of the ``add`` command above, which reads the networks from a
file (one per line). For example, given the following file:

networks.txt
  ::

    198.18.0.0/24
    198.18.1.0/24
    10.1/16
    10/16

These networks could be added like so::

  $ netcalc add-file networks.txt
  10.0.0.0/15
  198.18.0.0/23

sub command
...........

Subtract a network from another, splitting as necessary. ::

  $ netcalc sub 192.0.2.0/24 192.0.2.0/28
  192.0.2.16/28
  192.0.2.32/27
  192.0.2.64/26
  192.0.2.128/25

split command
.............

Split a network into subnets of a certain length. ::

  $ netcalc split 198.18.64.0/18 20
  198.18.64.0/20
  198.18.80.0/20
  198.18.96.0/20
  198.18.112.0/20

It is also possible to do a hierarchical split, showing all the steps from a
certain length to a specified maximum length::

  $ netcalc split 198.18.64.0/18 19 21
  198.18.64.0/19
    198.18.64.0/20
      198.18.64.0/21
      198.18.72.0/21
    198.18.80.0/20
      198.18.80.0/21
      198.18.88.0/21
  198.18.96.0/19
    198.18.96.0/20
      198.18.96.0/21
      198.18.104.0/21
    198.18.112.0/20
      198.18.112.0/21
      198.18.120.0/21

expr command
............

Add and subtract networks using an arbitrarily long mathematical expression. ::

  $ netcalc expr 2001:db8::/34 - 2001:db8::/38 + 2001:db8:100::/41
  2001:db8:100::/41
  2001:db8:400::/38
  2001:db8:800::/37
  2001:db8:1000::/36
  2001:db8:2000::/35

info command
............

Provide static information about a network. Shows the network address, netmask,
first and last addresses, and so on. ::

  $ netcalc info 2001:db8::8000:0:0:a:5/56
  Compact address   - 2001:db8:0:8000::a:5
  Expanded address  - 2001:0db8:0000:8000:0000:0000:000a:0005
  Address type      - Global Unicast
  Network address   - 2001:db8:0:8000::/56
  Network mask      - ffff:ffff:ffff:ff00:0:0:0:0
  Prefix length     - 56
  Host wildcard     - 0:0:0:ff:ffff:ffff:ffff:ffff
  Broadcast address - N/A
  Address count     - 4722366482869645213696
  First address     - 2001:0db8:0000:8000:0000:0000:0000:0000
  Last address      - 2001:0db8:0000:80ff:ffff:ffff:ffff:ffff


Expanding arguments from a text file
....................................

It is possible to expand command-line arguments from a text file, for any
command, by referencing the filename with a ``@`` placeholder. The file's
contents will be read and inserted as though they had been typed at the
command-line. Each line of text will turn into a separate command line
argument.

Argument expansion is useful for commands which don't already support receiving
a filename from which to read their arguments. Using this, it is possible for
example to calculate an arbitrarily long expression with the ``expr`` command.

For example, given the following file:

/tmp/math-arguments.txt
  ::

    2001:db8::/34
    -
    2001:db8::/38
    +
    2001:db8:100::/41

This expression could be calculated like so::

    $ netcalc expr @/tmp/math-arguments.txt
    2001:db8:100::/41
    2001:db8:400::/38
    2001:db8:800::/37
    2001:db8:1000::/36
    2001:db8:2000::/35

It is even possible (albeit perhaps farfetched) to specify the actual command
within the argument file:

/tmp/arguments.txt
  ::

    sub
    10.0.0.0/24
    10.0.0.64/27

Which would yield::

  $ netcalc @arguments.txt
  10.0.0.0/26
  10.0.0.96/27
  10.0.0.128/25

Of course, it would also be possible to use argument expansion to read networks
from a file as arguments into the ``add`` command. However, this would be rather
redundant, as it is equivalent to just using the ``add-file`` command,
exemplified above.

Given the file:

networks.txt
  ::

    198.18.0.0/24
    198.18.1.0/24
    10.1/16
    10/16

These networks could be added like so::

    $ netcalc add @networks.txt
    10.0.0.0/15
    198.18.0.0/23


Installing
----------

Using pip
.........

The easiest way to install NetCalc is through the official
`Python Package Index`_, using a package manager such as pip_::

    $ sudo pip install netcalc

This will install NetCalc globally, and take care of installing all necessary
dependencies first.

It is also possible to install only to the local user's environment, without
changing the global system::

    $ pip install --user netcalc

This will install NetCalc in the user's environment, which can be e.g. in
``~/.local`` in GNU/Linux, UNIX and Mac OSX, or ``%APPDATA%\Python`` in
Windows. You will need to run ``netcalc`` from within the user environment: on
GNU/Linux for example, this will be ``~/.local/bin/netcalc``.

From source
...........

NetCalc can also be run directly from the source directory, as long as the
requirements are already installed.

The only requirement is netaddr_. On a Debian or Ubuntu system, install the
``python3-netaddr`` package (for Python 3), or ``python-netaddr`` (for Python
2). On a Gentoo system, install ``dev-python/netaddr``.

To run from source, just execute ``./netcalc.py`` from within the root of the
source directory::

    $ cd netcalc
    $ ./netcalc.py add 10.0.0.24/29 10.0.0.16/29
    10.0.0.16/28


Future plans
------------

Future plans for NetCalc include, in no particular order:

- new command for static information (netmask/bitmask, IP range)
- new command for WHOIS queries
- make expr command more generic, allow e.g. splitting subnets
- ability to read networks from file in different formats (CSV, etc.)
- create packages for common GNU/Linux distributions, and installer for Windows
- ???

Suggestions are quite welcome :)


Contact
-------

NetCalc is developed by Israel G. Lugo <israel.lugo@lugosys.com>. Main
repository for cloning, submitting issues and/or forking is at
https://github.com/israel-lugo/netcalc


License
-------

Copyright (C) 2016, 2017 Israel G. Lugo <israel.lugo@lugosys.com>

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
.. |PyPi version| image:: https://img.shields.io/pypi/v/netcalc.svg
   :target: https://pypi.python.org/pypi/netcalc
.. |PyPi pyversion| image:: https://img.shields.io/pypi/pyversions/netcalc.svg?maxAge=86400
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/4479f8bd8ddd4ba58c09867bf97133cd
   :target: https://www.codacy.com/app/israel-lugo/netcalc
.. _netaddr: https://github.com/drkjam/netaddr
.. _Python Package Index: https://pypi.python.org/pypi/netcalc/
.. _pip: https://pip.pypa.io/en/stable/


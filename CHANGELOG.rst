NetCalc Change Log
==================

All releases and notable changes will be described here.

NetCalc adheres to `semantic versioning <http://semver.org>`_. In short, this
means the version numbers follow a three-part scheme: *major version*, *minor
version* and *patch number*.

The *major version* is incremented for releases that break compatibility, such
as removing or altering existing functionality. The *minor version* is
incremented for releases that add new visible features, but are still backwards
compatible. The *patch number* is incremented for minor changes such as bug
fixes, that don't change the public interface.


Unreleased__
------------
__ https://github.com/israel-lugo/netcalc/compare/v0.6.1...HEAD


0.6.1_ — 2017-02-07
-------------------

Changed
.......

- Relax ``netaddr`` version requirement to >= 0.7.12 (from 0.7.18). The older
  version still works, and it's the one that comes with Debian Jessie.


0.6.0_ — 2017-02-05
-------------------

Added
.....

- New command ``info``. Provides static information on a subnet, e.g. network
  address, netmask, first and last addresses, and so on. See `issue #3`_.


0.5.0_ — 2017-01-15
-------------------

Added
.....

- New argument for the ``split`` command, to do a hierarchical split. Shows all
  the steps from a certain length to a specified maximum length. See
  `issue #7`_.


0.4.0_ — 2016-11-18
-------------------

Added
.....

- New command ``add-file``. Works like ``add``, but reads the list of networks
  from a file (one per line). See `issue #2`_.


0.3.1_ — 2016-11-13
-------------------

Added
.....

- Created installation instructions on the README.


0.3.0_ — 2016-11-12
-------------------

Added
.....

- New command ``split``. Allows splitting a network into subnets of a certain
  length.


0.2.0_ — 2016-11-06
-------------------

Added
.....

- Arguments can be specified from a text file, one per line. This makes it
  possible e.g. to specify multiple networks to an ``add`` command. See
  `issue #2`_.


0.1.0_ — 2016-11-01
-------------------

First production release.

.. _issue #2: https://github.com/israel-lugo/netcalc/issues/2
.. _issue #3: https://github.com/israel-lugo/netcalc/issues/3
.. _issue #7: https://github.com/israel-lugo/netcalc/issues/7

.. _0.6.1: https://github.com/israel-lugo/netcalc/tree/v0.6.1
.. _0.6.0: https://github.com/israel-lugo/netcalc/tree/v0.6.0
.. _0.5.0: https://github.com/israel-lugo/netcalc/tree/v0.5.0
.. _0.4.0: https://github.com/israel-lugo/netcalc/tree/v0.4.0
.. _0.3.1: https://github.com/israel-lugo/netcalc/tree/v0.3.1
.. _0.3.0: https://github.com/israel-lugo/netcalc/tree/v0.3.0
.. _0.2.0: https://github.com/israel-lugo/netcalc/tree/v0.2.0
.. _0.1.0: https://github.com/israel-lugo/netcalc/tree/v0.1.0

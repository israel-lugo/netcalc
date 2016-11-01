
"""Package information for NetCalc."""

import os.path
import io

from setuptools import setup

from netcalc.version import __version__


def read(file_path_components, encoding="utf8"):
    """Read the contents of a file.

    Receives a list of path components to the file and joins them in an
    OS-agnostic way. Opens the file for reading using the specified
    encoding, and returns the file's contents.

    Works both in Python 2 and Python 3.

    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *file_path_components),
        encoding=encoding
    ) as fp:
        return fp.read()


setup(
    name='netcalc',
    description='Advanced network calculator and address planning helper',
    author="Israel G. Lugo",
    author_email='israel.lugo@lugosys.com',
    url='https://github.com/israel-lugo/netcalc',
    version=__version__,
    packages=['netcalc'],
    install_requires=[ 'netaddr>=0.7.18' ],
    entry_points={
        'console_scripts': [ 'netcalc=netcalc.cli:main' ],
    },
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Documentation',
        'Topic :: Education ',
        'Topic :: Internet',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Firewalls ',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    long_description=read([ "README.rst" ])
)

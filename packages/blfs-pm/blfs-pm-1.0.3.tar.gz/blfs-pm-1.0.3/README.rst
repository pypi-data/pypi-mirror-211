BLFS-automation:
================

“A simple Python package that simplifies your BLFS project in many
ways…”

About this project:
-------------------

This project is designed for people who have built their own
LinuxFromScratch (LFS) system, and are now working on the next stage -
BeyondLinuxFromScratch (BLFS). BLFS packages often require many other
dependencies to work, and sometimes it is a bit cumbersome to install
all of those. ``blfs-pm`` aims to make it easier to install these
packages without the stress of downloading everything and calculating,
while simultaneously allowing you to still get the full build
experience.

Download and installation:
--------------------------

To get a local copy up and running follow these steps.

Prerequisites:
~~~~~~~~~~~~~~

.. raw:: html

   <ul>

.. raw:: html

   <li>

A working LFS system (check them out at
https://www.linuxfromscratch.org/)

.. raw:: html

   </li>

.. raw:: html

   <li>

A working internet connection - you may need to install a couple of BLFS
packages like NetworkManager, DHCPClient, and WPA-supplicant.

.. raw:: html

   </li>

.. raw:: html

   <li>

A working Python environment

.. raw:: html

   </li>

.. raw:: html

   <li>

Python3 package manager (Pip)

.. raw:: html

   </li>

.. raw:: html

   <li>

Git (https://www.linuxfromscratch.org/blfs/view/svn/general/git.html)

.. raw:: html

   </li>

.. raw:: html

   </ul>

Installation:
~~~~~~~~~~~~~

::

   pip install blfs-pm

Usage:
------

It is recommended that the package should always be run as root, in
order to prevent errors when installing packages to the system.

This package has many options to list, download, list commands, or
install a given package. Note: once again it is *highly* recommended
that you always run this as ``root``!

Usage:
``blfs-pm [-h] [-a] [-b PACKAGE] [-c PACKAGE] [-d PACKAGE] [-f] [-l PACKAGE] [-o] [-r] [-s PACKAGE] [--systemd]``

Note: It is recommended to follow along the installation process in the
BLFS book. ``blfs-pm`` is not perfect and I have not tested every BLFS
package. There are still some issues with circular dependencies, and at
the moment it is best to monitor everything to prevent problems.
Additionally, the ``-b (build)`` option will prompt the user to run
EVERY command provided for the specific package. Some commands can only
be run if optional dependencies are installed (like Texlive, Docbook,
etc.). Furthermore, some packages require further kernel configuration
(and recompilation) as a prerequisite for installation.

::

     -h, --help                        show this help message and exit

     -a, --all                         Downloads ALL BLFS packages - uses a lot of time and space.

     -b PACKAGE, --build PACKAGE       Install a given Package on the system.

     -c PACKAGE, --commands PACKAGE    List installation (without installing) commands for a given package.
     
     -d PACKAGE, --download PACKAGE    Downloads a given BLFS package along with all of its dependencies.

     -f, --force                       Force package installation even though it is already installed

     -l PACKAGE, --list PACKAGE        Lists all of the dependencies for a given BLFS package in order of installation.

     -o, --optional                    List/download optional packages.

     -r, --recommended                 List/download recommended packages.

     -s PACKAGE, --search PACKAGE      Search for a given package.
     --systemd                         Pass this flag if you built LFS with Systemd

Additional options:
-------------------

Contributers:
-------------

Ahron Maslin (creator, maintainer, and designer), Josh W. (moral
support), Dan the Man (Chief Psychologist)

Todo
----

-  [ ] implement different db’s for different LFS versions
-  [ ] add ``--info`` flag to display information about a package
-  [ ] query to install a package if only one search result was found

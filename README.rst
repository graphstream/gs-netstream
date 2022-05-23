=============
NetStream
=============

Netstream is basically a network protocol aiming at opening the `GraphStream`_ project access to other tools/projects/programs especially those written in other languages than Java. The interface is managed through a network interface (client/server approach) 

The aim of this gs-netstream project is to propose a repository of implementations of the protocol, written in various languages.  

.. _GraphStream: http://graphstream-project.org/

Implementations of the NetStream protocol can be from the sender (client) side so as from the receiver (server) side.  

For now here are the implementations that are proposed:

- a python sender
- a C++ sender
- a Java sender with no dependency to gs-core (useful for java projects that don't want any dependency to the GS binaries)


If you need to implement a sender or a receiver in another language,
check the `manual`_ for a full description of the protocol

.. _manual: https://github.com/graphstream/gs-netstream/wiki/NetStream-Manual

Building for C++
----------------

For C++, you can build gs-netstream using the code in the `c++` directory. Just run 'make'.

This has been tested to build with gcc 11.2.0 on MSYS2 (as of Nov 2021) and with gcc 9.3 on Ubuntu 20.04. Only building was tested.

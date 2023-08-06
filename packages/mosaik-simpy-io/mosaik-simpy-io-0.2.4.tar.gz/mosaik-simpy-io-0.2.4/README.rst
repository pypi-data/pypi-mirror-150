mosaik-simpy-io
===============

*mosaik-simpy-io* is a fork of simpy.io_ to fix some problems for the use of simpy.io together with mosaik_.

.. _simpy.io: https://gitlab.com/team-simpy/simpy.io
.. _mosaik: https://mosaik.offis.de

Version: 0.2.4

License: MIT

simpy.io
--------

*simpy.io* is an asynchronous networking library based on SimPy_. The nature
of networking is thoroughly event-based (messages can for example be thought of
as events). *simpy.io* marries the solid event system of SimPy_ with
asynchronous input and output.

It provides several degrees of abstraction (raw sockets, packets and
request-reply messages), supports various back-ends ((e)poll, select, asyncore,
virtual) and lets you use different socket types, like TCP, SSL-encrypted,
simulated). Furthermore protocols like HTTP, WebSockets and an extensible RPC
interface are also supported.

.. _SimPy: http://simpy.readthedocs.org

Current status
--------------

simpy.io is currently in the early alpha phase of development. There is no
guarantee for API stability (modules will almost certainly be renamed before
the 1.0 release) and simpy.io may break on your system. Sadly, there isn't any
documentation available as of now (apart from the examples and tests).

The state of the individual modules is as follows:

* sockets: stable *alpha*
* packets: stable *alpha*
* message: stable *alpha*
* http: *draft*
* websockets: *draft*
* rpc: *draft*


Installation
------------

simpy.io requires Python between 3.5 and 3.9 and SimPy 3. You can install it from via pip:

.. sourcecode:: bash

    $ pip install mosaik-simpy-io

Examples
--------

The following three examples demonstrate simpy.io's levels of abstraction:

Socket level
^^^^^^^^^^^^

When working directly with simpy.io sockets, you can try to *read* and *write*
a specified number of bytes from or to a socket (note that there is no
guarantee from the OS that all data will be received or transmitted):

.. sourcecode:: python

    >>> from simpy.io import select as backend
    >>>
    >>> def server(env, addr):
    ...     server_sock = backend.TCPSocket.server(env, addr)
    ...     sock = yield server_sock.accept()
    ...     data = yield sock.read(4)
    ...     print(data.decode())
    ...     yield sock.write('cya'.encode())
    >>>
    >>> def client(env, addr):
    ...     sock = backend.TCPSocket.connection(env, addr)
    ...     yield sock.write('ohai'.encode())
    ...     data = yield sock.read(3)
    ...     print(data.decode())
    >>>
    >>> addr = ('127.0.0.1', 5555)
    >>> env = backend.Environment()
    >>> srv = env.process(server(env, addr))
    >>> cli = env.process(client(env, addr))
    >>> env.run(until=cli)
    ohai
    cya


Packet level
^^^^^^^^^^^^

simpy.io packets alleviate the limitation of raw sockets and allow you to read
and write complete packets. These can either be bytes (if you use ``Packet``)
or (unicode) strings (if you use ``PacketUTF8``):

.. sourcecode:: python

    >>> from simpy.io import select as backend
    >>> from simpy.io.packet import Packet
    >>>
    >>> def server(env, addr):
    ...     server_sock = backend.TCPSocket.server(env, addr)
    ...     sock = yield server_sock.accept()
    ...     packet = Packet(sock)
    ...     data = yield packet.read()
    ...     print(data.decode())
    ...     yield packet.write('cya'.encode())
    >>>
    >>> def client(env, addr):
    ...     packet = Packet(backend.TCPSocket.connection(env, addr))
    ...     yield packet.write('ohai'.encode())
    ...     data = yield packet.read()
    ...     print(data.decode())
    >>>
    >>> addr = ('127.0.0.1', 5556)
    >>> env = backend.Environment()
    >>> srv = env.process(server(env, addr))
    >>> cli = env.process(client(env, addr))
    >>> env.run(until=cli)
    ohai
    cya


Message level
^^^^^^^^^^^^^

The message level adds message counters that allow you to asynchronously send
messages (even concurrently) and maps replies to their proper requests.
Furthermore, you can specify (de)serializers (by default, *JSON* is used) and
replies can signal success/failure:

.. sourcecode:: python

    >>> from simpy.io import select as backend
    >>> from simpy.io.packet import PacketUTF8
    >>> from simpy.io.message import Message
    >>>
    >>> def server(env, addr):
    ...     server_sock = backend.TCPSocket.server(env, addr)
    ...     sock = yield server_sock.accept()
    ...     message = Message(env, PacketUTF8(sock))
    ...     request = yield message.recv()
    ...     print(request.content)
    ...     yield request.succeed('cya')
    >>>
    >>> def client(env, addr):
    ...     message = Message(env, PacketUTF8(
    ...             backend.TCPSocket.connection(env, addr)))
    ...     reply = yield message.send('ohai')
    ...     print(reply)
    >>>
    >>> addr = ('127.0.0.1', 5557)
    >>> env = backend.Environment()
    >>> srv = env.process(server(env, addr))
    >>> cli = env.process(client(env, addr))
    >>> env.run(until=cli)
    ohai
    cya

Help & Contact
--------------

Bugs should be posted on our `issue tracker`__ here on GitLab.

__ https://gitlab.com/mosaik/tools/simpy.io/-/issues/new

# -*- encoding: utf-8 -*-


from asyncio import Protocol, get_running_loop, run
from asyncio.transports import BaseTransport


class EchoServerProtocol(Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport: BaseTransport) -> None:
        peerinfo = transport.get_extra_info('peername')
        print(f"connection from {peerinfo}")
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = get_running_loop()
    # transport, protocol

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888
    )

    async with server:
        await server.serve_forever()


run(main())

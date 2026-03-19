from asyncio import StreamReader, StreamWriter
from typing import Set, Tuple
import asyncio
import logging
import abc

logging.basicConfig(level=logging.DEBUG)


class TcpServer:
    ip: str
    port: int

    logger: logging.Logger

    clients: Set['TcpHandler']

    def __init__(self, cls, ip: str, port: int):
        self.cls = cls

        self.ip = ip
        self.port = port

        self.logger = logging.getLogger('Server')

        self.logger.setLevel(logging.DEBUG)

        self.clients = set()

        self.logger.info('Initialized')

    async def broadcast(self, sender: 'TcpHandler', data, ignore_sender: bool = True) -> None:
        for client in self.clients.copy():
            if not client.is_broadcastable() or (ignore_sender and client is sender):
                continue

            try:
                await client.send_broadcast(data)
            except ConnectionResetError:
                self.clients.remove(client)

    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        client = self.cls(self, reader, writer)

        await client.handle()

        await client.finish()

    async def loop(self) -> None:
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)

        async with server:
            await server.serve_forever()

    def run(self) -> None:
        self.logger.info(f'Listening on {self.ip}:{self.port}')

        try:
            asyncio.run(self.loop())
        except KeyboardInterrupt:
            pass


class TcpHandler(metaclass=abc.ABCMeta):
    server: 'TcpServer'
    reader: StreamReader
    writer: StreamWriter

    ip: str
    port: int

    logger: logging.Logger

    def __init__(self, server: 'TcpServer', reader: StreamReader, writer: StreamWriter):
        self.server = server
        self.reader = reader
        self.writer = writer

        self.server.clients.add(self)

        self.ip, self.port = self.writer.get_extra_info('peername')

        self.logger = logging.getLogger(f'Client {self.ip}:{self.port}')

        self.logger.setLevel(logging.DEBUG)

        self.logger.info('Connected')

    @abc.abstractmethod
    async def handle(self) -> None:
        raise NotImplementedError

    async def finish(self) -> None:
        self.writer.close()

        await self.writer.wait_closed()

        self.server.clients.remove(self)

        self.logger.info('Disconnected')

    async def broadcast(self, data, ignore_self: bool = True) -> None:
        await self.server.broadcast(self, data, ignore_sender=ignore_self)

    async def send_broadcast(self, data) -> None:
        raise NotImplementedError('Must be implemented')

    def is_broadcastable(self) -> bool:
        raise NotImplementedError('Must be implemented')


class UdpServer:
    ip: str
    port: int

    logger: logging.Logger

    def __init__(self, cls, ip: str, port: int):
        self.cls = cls

        self.ip = ip
        self.port = port

        self.logger = logging.getLogger('Server')

        self.logger.setLevel(logging.DEBUG)

        self.logger.info('Initialized')

    def handle_client(self):
        return self.cls(self)

    async def loop(self):
        loop = asyncio.get_running_loop()

        return await loop.create_datagram_endpoint(self.handle_client, (self.ip, self.port))

    def run(self) -> None:
        self.logger.info(f'Listening on {self.ip}:{self.port}')

        loop = asyncio.get_event_loop()

        (transport, protocol) = loop.run_until_complete(self.loop())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        loop.close()


class UdpHandler(metaclass=abc.ABCMeta):
    server: 'UdpServer'
    transport: asyncio.DatagramTransport

    addr: Tuple[str, int]

    logger: logging.Logger

    def __init__(self, server: 'UdpServer'):
        self.server = server

    @abc.abstractmethod
    def handle(self, data: bytes) -> None:
        raise NotImplementedError

    def connection_made(self, transport: asyncio.DatagramTransport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]):
        self.addr = addr

        self.logger = logging.getLogger(f'Client {self.addr[0]}:{self.addr[1]}')

        self.logger.setLevel(logging.DEBUG)

        self.logger.info('Connected')

        self.handle(data)

    def connection_lost(self, exc):
        self.logger.info('Disconnected')


def run_server(server_cls, client_cls) -> None:
    server = server_cls(client_cls, '0.0.0.0', 64444)

    server.run()

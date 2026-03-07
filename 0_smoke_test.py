from asyncio import StreamReader, StreamWriter
from support import protohackers


async def smoke_test(reader: StreamReader, writer: StreamWriter) -> None:
    while True:
        data = await reader.read(1)

        if not data:
            break

        writer.write(data)

        await writer.drain()


if __name__ == '__main__':
    protohackers.run_server(smoke_test)

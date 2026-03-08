from asyncio import StreamReader, StreamWriter
from support import protohackers


async def smoke_test(reader: StreamReader, writer: StreamWriter) -> None:
    logger = protohackers.create_logger(writer)

    data = await reader.read()

    logger.debug(f'>> {data}')

    writer.write(data)

    await writer.drain()

    logger.debug(f'<< {data}')

    writer.close()

    await writer.wait_closed()

    logger.info('Disconnected')


if __name__ == '__main__':
    protohackers.run_server(smoke_test)

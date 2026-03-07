from typing import Callable, Coroutine, Any
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)


def create_logger(writer: asyncio.StreamWriter) -> logging.Logger:
    ip, port = writer.get_extra_info('peername')

    logger = logging.getLogger(f'{ip}:{port}')

    logger.setLevel(logging.DEBUG)

    return logger


def run_server(callback: Callable[[asyncio.StreamReader, asyncio.StreamWriter], Coroutine[Any, Any, None]]) -> None:
    ip = '0.0.0.0'
    port = 64444

    async def main_loop():
        server = await asyncio.start_server(callback, ip, port)

        async with server:
            await server.serve_forever()

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        pass

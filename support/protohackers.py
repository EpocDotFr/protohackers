from typing import Callable, Coroutine, Any
import asyncio


def run_server(callback: Callable[[asyncio.StreamReader, asyncio.StreamWriter], Coroutine[Any, Any, None]]) -> None:
    ip = '0.0.0.0'
    port = 64444

    async def main():
        server = await asyncio.start_server(callback, ip, port)

        async with server:
            await server.serve_forever()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

from support import protohackers


class SmokeTestHandler(protohackers.TcpHandler):
    async def handle(self) -> None:
        data = await self.reader.read()

        self.logger.debug(f'>> {data}')

        self.writer.write(data)

        await self.writer.drain()

        self.logger.debug(f'<< {data}')


if __name__ == '__main__':
    protohackers.run_server(protohackers.TcpServer, SmokeTestHandler)

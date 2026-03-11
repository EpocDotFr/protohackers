from typing import Any, OrderedDict
from support import protohackers
from json import JSONDecodeError
import json


class PrimeTimeHandler(protohackers.TcpHandler):
    async def handle(self) -> None:
        while True:
            data = (await self.reader.readline()).decode('ascii').strip()

            if not data:
                break

            self.logger.debug(f'>> {data}')

            try:
                if not data.startswith('{') or not data.endswith('}'):
                    raise ValueError()

                json_data = json.loads(data)

                is_malformed_request = 'method' not in json_data or \
                                       'number' not in json_data or \
                                       json_data['method'] != 'isPrime' or \
                                       not isinstance(json_data['number'], (int, float)) or \
                                       isinstance(json_data['number'], bool)

                if is_malformed_request:
                    raise ValueError()

                await self.send_response(
                    is_prime(json_data['number']) if isinstance(json_data['number'], int) else False
                )
            except (JSONDecodeError, ValueError):
                await self.send_error()

                break

    async def send_response(self,prime: bool) -> None:
        await self.send(OrderedDict([
            ('method', 'isPrime'),
            ('prime', prime),
        ]))

    async def send_error(self) -> None:
        await self.send(OrderedDict([
            ('method', 'error'),
        ]))

    async def send(self, data: Any) -> None:
        data = json.dumps(data) + '\n'

        self.writer.write(data.encode('utf-8'))

        await self.writer.drain()

        self.logger.debug(f'<< {data}')


def is_prime(n: int) -> bool:
    if abs(n) == 1:
        return False
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True


if __name__ == '__main__':
    protohackers.run_server(protohackers.TcpServer, PrimeTimeHandler)

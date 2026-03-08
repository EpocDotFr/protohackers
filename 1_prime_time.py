from asyncio import StreamReader, StreamWriter
from support import protohackers
from json import JSONDecodeError
import json


async def prime_time(reader: StreamReader, writer: StreamWriter) -> None:
    logger = protohackers.create_logger(writer)

    while True:
        data = (await reader.readline()).decode('ascii').strip()

        if not data:
            writer.close()

            await writer.wait_closed()

            break

        logger.debug(f'>> {data}')

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

            writer.write((json.dumps({'method': 'isPrime', 'prime': is_prime(json_data['number']) if isinstance(json_data['number'], int) else False}) + '\n').encode('utf-8'))

            await writer.drain()
        except (JSONDecodeError, ValueError):
            writer.write((json.dumps({'method': 'error'}) + '\n').encode('utf-8'))

            await writer.drain()

            writer.close()

            await writer.wait_closed()

            break


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
    protohackers.run_server(prime_time)

from asyncio import StreamReader, StreamWriter, IncompleteReadError
from collections import OrderedDict
from support import protohackers
import statistics
import struct


async def means_to_and_end(reader: StreamReader, writer: StreamWriter) -> None:
    prices = OrderedDict()

    logger = protohackers.create_logger(writer)

    while True:
        try:
            message_type, int_1, int_2 = struct.unpack('!cii', await reader.readexactly(9))
        except (struct.error, IncompleteReadError):
            writer.close()

            await writer.wait_closed()

            break

        if not message_type:
            writer.close()

            await writer.wait_closed()

            break

        logger.debug(f'>> {message_type} {int_1} {int_2}')

        if message_type == b'I':
            timestamp, price = int_1, int_2

            if timestamp not in prices:
                prices[timestamp] = price
        elif message_type == b'Q':
            mintime, maxtime = int_1, int_2
            mean = 0

            if mintime <= maxtime:
                prices = OrderedDict(sorted(prices.items(), key=lambda item: item[0]))

                prices_for_mean = [price for timestamp, price in prices.items() if mintime <= timestamp <= maxtime]

                if prices_for_mean:
                    mean = int(statistics.mean(prices_for_mean))

            writer.write(struct.pack('!i', mean))

            await writer.drain()


if __name__ == '__main__':
    protohackers.run_server(means_to_and_end)

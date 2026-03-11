from asyncio import IncompleteReadError
from collections import OrderedDict
from support import protohackers
import statistics
import struct


class MeansToAnEndHandler(protohackers.TcpHandler):
    prices: OrderedDict

    def __init__(self, *args, **kvargs):
        super(MeansToAnEndHandler, self).__init__(*args, **kvargs)

        self.prices = OrderedDict()

    async def handle(self) -> None:
        while True:
            try:
                message_type, int_1, int_2 = struct.unpack('!cii', await self.reader.readexactly(9))
            except (struct.error, IncompleteReadError):
                break

            if not message_type:
                break

            self.logger.debug(f'>> {message_type} {int_1} {int_2}')

            if message_type == b'I':
                timestamp, price = int_1, int_2

                if timestamp not in self.prices:
                    self.prices[timestamp] = price
            elif message_type == b'Q':
                mintime, maxtime = int_1, int_2
                mean = 0

                if mintime <= maxtime:
                    prices = OrderedDict(sorted(self.prices.items(), key=lambda item: item[0]))

                    prices_for_mean = [price for timestamp, price in prices.items() if mintime <= timestamp <= maxtime]

                    if prices_for_mean:
                        mean = int(statistics.mean(prices_for_mean))

                self.writer.write(struct.pack('!i', mean))

                await self.writer.drain()


if __name__ == '__main__':
    protohackers.run_server(protohackers.TcpServer, MeansToAnEndHandler)

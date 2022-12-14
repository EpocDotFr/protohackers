from collections import OrderedDict
from support import protohackers
import statistics
import struct


class MeansToAnEndHandler(protohackers.TCPHandler):
    def setup(self):
        super(MeansToAnEndHandler, self).setup()

        self.prices = OrderedDict()

    def handle(self):
        while True:
            try:
                message_type, int_1, int_2 = struct.unpack('!cii', self.rfile.read(9))
            except struct.error:
                break

            if not message_type:
                break

            if message_type == b'I':
                timestamp, price = int_1, int_2

                if timestamp not in self.prices:
                    self.prices[timestamp] = price
            elif message_type == b'Q':
                mintime, maxtime = int_1, int_2
                mean = 0

                if mintime <= maxtime:
                    self.prices = OrderedDict(sorted(self.prices.items(), key=lambda item: item[0]))

                    prices_for_mean = [price for timestamp, price in self.prices.items() if mintime <= timestamp <= maxtime]

                    if prices_for_mean:
                        mean = int(statistics.mean(prices_for_mean))

                self.wfile.write(struct.pack('!i', mean))


if __name__ == '__main__':
    protohackers.run_server(MeansToAnEndHandler, protohackers.TCPServer)

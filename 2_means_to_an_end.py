from collections import OrderedDict
import protohackers
import statistics


class MeansToAnEndHandler(protohackers.Handler, protohackers.HasDataStreamsHandlerMixin):
    def setup(self):
        super(MeansToAnEndHandler, self).setup()

        self.prices = OrderedDict()

    def handle(self):
        while True:
            message_type = self.rstream.read_byte()

            if not message_type:
                break

            if message_type == b'I':
                timestamp = self.rstream.read_int32()
                price = self.rstream.read_int32()

                if timestamp not in self.prices:
                    self.prices[timestamp] = price
            elif message_type == b'Q':
                mintime = self.rstream.read_int32()
                maxtime = self.rstream.read_int32()

                mean = 0

                if mintime <= maxtime:
                    self.prices = OrderedDict(sorted(self.prices.items(), key=lambda item: item[0]))

                    prices_for_mean = [price for timestamp, price in self.prices.items() if mintime <= timestamp <= maxtime]

                    if prices_for_mean:
                        mean = int(statistics.mean(prices_for_mean))

                self.wstream.write_int32(mean)


protohackers.run_server(MeansToAnEndHandler)

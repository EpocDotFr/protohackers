from protohacker_server import ProtohackerHandler, run_server
from data_stream import DataStream


class MeansToAnEndHandler(ProtohackerHandler):
    MESSAGE_INSERT = b'I'
    MESSAGE_QUERY = b'Q'

    def setup(self):
        super(MeansToAnEndHandler, self).setup()

        self.rstream = DataStream(self.rfile, DataStream.BSA_NETWORK)
        self.wstream = DataStream(self.wfile, DataStream.BSA_NETWORK)
        self.prices = {}

    def handle(self):
        while True:
            message_type = self.rstream.read_byte()

            print(message_type)

            if message_type == MeansToAnEndHandler.MESSAGE_INSERT:
                timestamp = self.rstream.read_int32()
                price = self.rstream.read_int32()

                if timestamp not in self.prices:
                    self.prices[timestamp] = price
            elif message_type == MeansToAnEndHandler.MESSAGE_QUERY:
                mintime = self.rstream.read_int32()
                maxtime = self.rstream.read_int32()

                mean = 0

                self.wstream.write_int32(mean)


run_server(MeansToAnEndHandler)

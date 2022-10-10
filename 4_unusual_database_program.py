from support import protohackers


class UnusualDatabaseProgramServer(protohackers.UDPServer):
    def __init__(self, *args, **kvargs):
        super(UnusualDatabaseProgramServer, self).__init__(*args, **kvargs)

        self.data = {
            b'version': b'Next Gen Redis/1.0'
        }


class UnusualDatabaseProgramHandler(protohackers.UDPHandler):
    def handle(self):
        if len(self.packet) >= 1000:
            return

        packet = self.packet.split(b'=', maxsplit=1)

        self.log(packet)

        if len(packet) == 1:  # Retrieve
            key, = packet
            value = self.server.data.get(key, b'')

            self.send_response(key, value)
        else:  # Insert
            key, value = packet

            if key == b'version':
                return

            self.server.data[key] = value

    def send_response(self, key, value):
        packet = [key, value]

        self.log(packet, inbound=False)

        self.respond(b'='.join(packet))


if __name__ == '__main__':
    protohackers.run_server(UnusualDatabaseProgramHandler, UnusualDatabaseProgramServer)

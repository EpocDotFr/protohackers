from support import protohackers
from typing import Dict


class UnusualDatabaseProgramServer(protohackers.UdpServer):
    data: Dict[bytes, bytes]

    def __init__(self, *args, **kvargs):
        super(UnusualDatabaseProgramServer, self).__init__(*args, **kvargs)

        self.data = {
            b'version': b'Next Gen Redis/1.0'
        }


class UnusualDatabaseProgramHandler(protohackers.UdpHandler):
    def handle(self, data: bytes) -> None:
        if len(data) >= 1000:
            return

        data = data.split(b'=', maxsplit=1)

        self.logger.debug(f'>> {data}')

        if len(data) == 1:  # Retrieve
            key, = data
            value = self.server.data.get(key, b'')

            self.send_response(key, value)
        else:  # Insert
            key, value = data

            if key == b'version':
                return

            self.server.data[key] = value

    def send_response(self, key, value):
        data = [key, value]

        self.logger.debug(f'<< {data}')

        self.transport.sendto(b'='.join(data), self.addr)


if __name__ == '__main__':
    protohackers.run_server(UnusualDatabaseProgramServer, UnusualDatabaseProgramHandler)

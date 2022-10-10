from collections import OrderedDict
from support import protohackers
from json import JSONDecodeError
import json


class PrimeTimeHandler(protohackers.TCPHandler):
    def handle(self):
        while True:
            data = self.rfile.readline().decode('ascii').strip()

            if not data:
                break

            self.log(data)

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

                self.send_response(
                    is_prime(json_data['number']) if isinstance(json_data['number'], int) else False
                )
            except (JSONDecodeError, ValueError):
                self.send_error()

                break

    def send_response(self, prime):
        self.send(OrderedDict([
            ('method', 'isPrime'),
            ('prime', prime),
        ]))

    def send_error(self):
        self.send(OrderedDict([
            ('method', 'error'),
        ]))

    def send(self, data):
        data = json.dumps(data) + '\n'

        self.wfile.write(data.encode('utf-8'))


def is_prime(n):
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
    protohackers.run_server(PrimeTimeHandler, protohackers.TCPServer)

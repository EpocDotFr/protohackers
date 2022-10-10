from support import protohackers


class SmokeTestHandler(protohackers.TCPHandler):
    def handle(self):
        while True:
            data = self.rfile.read(1)

            self.log(data)

            if not data:
                break

            self.wfile.write(data)


if __name__ == '__main__':
    protohackers.run_server(SmokeTestHandler, protohackers.TCPServer)

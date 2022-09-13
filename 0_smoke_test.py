from protohacker_server import ProtohackerHandler, run_server


class SmokeTestHandler(ProtohackerHandler):
    def handle(self):
        data = self.rfile.readline()

        if not data:
            return

        print('{}:{} >> {}'.format(self.client_address[0], self.client_address[1], data))

        self.wfile.write(data)


run_server(SmokeTestHandler)

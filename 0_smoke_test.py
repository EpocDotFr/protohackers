from protohacker_server import ProtohackerHandler, run_server


class SmokeTestHandler(ProtohackerHandler):
    def handle(self):
        while True:
            data = self.rfile.read(1)

            self.log_data(data)

            if not data:
                break

            self.wfile.write(data)


run_server(SmokeTestHandler)

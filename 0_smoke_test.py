from protohacker_server import ProtohackerHandler, run_server


class SmokeTestHandler(ProtohackerHandler):
    def handle(self):
        while True:
            data = self.rfile.readline()

            if not data:
                break

            self.log_data(data)

            self.wfile.write(data)


run_server(SmokeTestHandler)

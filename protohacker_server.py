from data_stream import DataStream
import socketserver


class ProtohackerServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class ProtohackerHandler(socketserver.StreamRequestHandler):
    def setup(self):
        super(ProtohackerHandler, self).setup()

        self.rstream = DataStream(self.rfile, DataStream.BSA_NETWORK)
        self.wstream = DataStream(self.wfile, DataStream.BSA_NETWORK)

    def handle(self):
        raise NotImplementedError('Must be implemented')

    def log(self, data):
        ip, port = self.client_address

        print('{}:{} >> {}'.format(ip, port, data))


def run_server(handler_class, server_class=ProtohackerServer):
    ip = '0.0.0.0'
    port = 1664

    with server_class((ip, port), handler_class) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

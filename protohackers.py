from data_stream import DataStream
import socketserver


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class Handler(socketserver.StreamRequestHandler):
    bsa = DataStream.BSA_NETWORK

    def setup(self):
        super(Handler, self).setup()

        self.rstream = DataStream(self.rfile, self.bsa)
        self.wstream = DataStream(self.wfile, self.bsa)

    def handle(self):
        raise NotImplementedError('Must be implemented')

    def log(self, data):
        ip, port = self.client_address

        print(f'{ip}:{port} >> {data}')


def run_server(handler_class, server_class=Server):
    ip = '0.0.0.0'
    port = 1664

    with server_class((ip, port), handler_class) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

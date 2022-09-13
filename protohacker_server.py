import socketserver


class ProtohackerServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class ProtohackerHandler(socketserver.StreamRequestHandler):
    def handle(self):
        raise NotImplementedError('Must be implemented')

    def log_data(self, data):
        print('{}:{} >> {}'.format(self.client_address[0], self.client_address[1], data))


def run_server(handler_class, server_class=ProtohackerServer):
    ip = '0.0.0.0'
    port = 1664

    with server_class((ip, port), handler_class) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

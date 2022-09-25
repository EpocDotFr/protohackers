from data_stream import DataStream
import socketserver


class ClientsAwareServerMixin:
    def __init__(self, *args, **kvargs):
        super(ClientsAwareServerMixin, self).__init__(*args, **kvargs)

        self.clients = set()

    def broadcast(self, sender, data, ignore_sender=True):
        for client in self.clients.copy():
            if not client.is_broadcastable() or (ignore_sender and client is sender):
                continue

            client.send_broadcast(data)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


class HasDataStreamsHandlerMixin:
    bsa = DataStream.BSA_NETWORK

    def setup(self):
        super(HasDataStreamsHandlerMixin, self).setup()

        self.rstream = DataStream(self.rfile, self.bsa)
        self.wstream = DataStream(self.wfile, self.bsa)


class ClientsAwareHandlerMixin:
    def setup(self):
        super(ClientsAwareHandlerMixin, self).setup()

        self.server.clients.add(self)

    def finish(self):
        self.server.clients.remove(self)

        super(ClientsAwareHandlerMixin, self).finish()

    def broadcast(self, data, ignore_self=True):
        self.server.broadcast(self, data, ignore_sender=ignore_self)

    def send_broadcast(self, data):
        raise NotImplementedError('Must be implemented')

    def is_broadcastable(self):
        raise NotImplementedError('Must be implemented')


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        raise NotImplementedError('Must be implemented')

    def log(self, data, inbound=True):
        ip, port = self.client_address

        chevrons = '>>' if inbound else '<<'

        print(f'{ip}:{port} {chevrons} {data}')


def run_server(handler_class, server_class=Server):
    ip = '0.0.0.0'
    port = 1664

    with server_class((ip, port), handler_class) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

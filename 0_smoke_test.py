import socketserver


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            data = self.rfile.read(1)

            if not data:
                break

            print('{}:{} >> {}'.format(self.client_address[0], self.client_address[1], data))

            self.wfile.write(data)


if __name__ == '__main__':
    with socketserver.ThreadingTCPServer(('0.0.0.0', 1664), Handler) as server:
        server.serve_forever()

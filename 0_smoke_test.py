import socketserver


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(self.rfile.read())


if __name__ == '__main__':
    with socketserver.ThreadingTCPServer(('0.0.0.0', 1664), Handler) as server:
        server.serve_forever()

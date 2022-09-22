import protohackers
import re

NAME_REGEX = re.compile(r'[^a-zA-Z0-9]')


class BudgetChatServer(protohackers.Server):
    def __init__(self, *args, **kvargs):
        super(BudgetChatServer, self).__init__(*args, **kvargs)

        self.clients = set()


class BudgetChatHandler(protohackers.Handler):
    def setup(self):
        super(BudgetChatHandler, self).setup()

        self.name = None

        self.server.clients.add(self)

    def handle(self):
        self.send_message('What is your name bruh?')

        name = self.get_message()

        self.log(name)

        if not name:
            return

        if NAME_REGEX.match(name) or not 1 <= len(name) <= 16:
            self.send_message('Invalid name provided')

            return

        self.name = name

        while True:
            message = self.get_message()

            if not message:
                break

            self.log(message)

    def finish(self):
        self.server.clients.remove(self)

        super(BudgetChatHandler, self).finish()

    def get_message(self):
        return self.rfile.readline().decode('ascii').strip()

    def send_message(self, message):
        self.wfile.write(''.join((message, '\n')).encode('ascii'))


protohackers.run_server(BudgetChatHandler, server_class=BudgetChatServer)

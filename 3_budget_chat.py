import protohackers
import re

NAME_REGEX = re.compile(r'^[a-zA-Z0-9]{1,16}$')


class BudgetChatServer(protohackers.ClientsAwareServerMixin, protohackers.Server):
    pass


class BudgetChatHandler(protohackers.ClientsAwareHandlerMixin, protohackers.Handler):
    def setup(self):
        super(BudgetChatHandler, self).setup()

        self.name = None

    def send_broadcast(self, data):
        self.send_message(data)

    def is_broadcastable(self):
        return True if self.name else False

    def handle(self):
        self.name = self.get_name()

        if not self.name:
            return

        self.send_chatters_list()
        self.broadcast(f'* {self.name} joined the chat')

        while True:
            message = self.receive_message()

            if not message:
                break

            self.broadcast(f'[{self.name}] {message}')

    def finish(self):
        if self.name:
            self.broadcast(f'* {self.name} left the chat')

        super(BudgetChatHandler, self).finish()

    def get_name(self):
        self.send_message('What\'s your name bruh?')

        name = self.receive_message()

        if not name:
            return False

        if not NAME_REGEX.search(name) or not 1 <= len(name) <= 16:
            self.send_message('Bruh, invalid name')

            return False

        return name

    def send_chatters_list(self):
        chatters_name = ', '.join(
            [client.name for client in self.server.clients.copy() if client.is_broadcastable() and client is not self]
        )

        chatters_name = chatters_name or 'nobody'

        self.send_message(f'* Hi bruh, now chatting with {chatters_name}')

    def receive_message(self):
        message = self.rfile.readline().decode('ascii').strip()

        self.log(message)

        return message

    def send_message(self, message):
        message = ''.join((message, '\n')).encode('ascii')

        self.log(message, inbound=False)

        self.wfile.write(message)


protohackers.run_server(BudgetChatHandler, BudgetChatServer)

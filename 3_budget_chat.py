from support import protohackers
from typing import Optional, Union
import re

NAME_REGEX = re.compile(r'^[a-zA-Z0-9]{1,16}$')


class BudgetChatHandler(protohackers.TcpHandler):
    name: Optional[str]

    def __init__(self, *args, **kvargs):
        super(BudgetChatHandler, self).__init__(*args, **kvargs)

        self.name = None

    async def send_broadcast(self, data) -> None:
        await self.send_message(data)

    def is_broadcastable(self) -> bool:
        return True if self.name else False

    async def handle(self) -> None:
        self.name = await self.get_name()

        if not self.name:
            return

        await self.send_chatters_list()
        await self.broadcast(f'* {self.name} joined the chat')

        while True:
            message = await self.receive_message()

            if not message:
                break

            await self.broadcast(f'[{self.name}] {message}')

    async def finish(self) -> None:
        if self.name:
            await self.broadcast(f'* {self.name} left the chat')

        await super(BudgetChatHandler, self).finish()

    async def get_name(self) -> Union[bool, str]:
        await self.send_message('What\'s your name mate?')

        name = await self.receive_message()

        if not name:
            return False

        if not NAME_REGEX.search(name) or not 1 <= len(name) <= 16:
            await self.send_message('Invalid name bro')

            return False

        return name

    async def send_chatters_list(self) -> None:
        chatters_name = ', '.join(
            [client.name for client in self.server.clients.copy() if client.is_broadcastable() and client is not self]
        )

        chatters_name = chatters_name or 'nobody'

        await self.send_message(f'* Hey, now chatting with {chatters_name}')

    async def receive_message(self) -> str:
        message = (await self.reader.readline()).decode('ascii').strip()

        self.logger.debug(f'>> {message}')

        return message

    async def send_message(self, message) -> None:
        message = ''.join((message, '\n')).encode('ascii')

        self.logger.debug(f'<< {message}')

        self.writer.write(message)

        await self.writer.drain()


if __name__ == '__main__':
    protohackers.run_server(protohackers.TcpServer, BudgetChatHandler)

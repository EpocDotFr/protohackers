from support import protohackers


class UnusualDatabaseProgramHandler(protohackers.UDPHandler):
    def handle(self):
        packet = self.packet.decode('utf-8').strip()

        if len(packet) >= 1000:
            return

        packet_parsed = packet.split('=', maxsplit=1)

        self.log(packet_parsed)

        if len(packet_parsed) == 1: # Retrieve
            pass
        else: # Insert
            pass


protohackers.run_server(UnusualDatabaseProgramHandler, protohackers.UDPServer)

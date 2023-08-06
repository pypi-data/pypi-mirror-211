import websocket, asyncio

class server(websocket):
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        pass

    def see(self):
        print(f'{self.ip}:{self.port}')
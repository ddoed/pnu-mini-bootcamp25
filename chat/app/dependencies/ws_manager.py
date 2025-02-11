# ws_manager.py
from fastapi import WebSocket

class WSManager:
    def __init__(self):
        # self.connections: list[WebSocket] = []
        self.conns: dict[str, WebSocket] = {}


    # 1. 클라이언트 연결요청 수락
    async def connect(self, ws: WebSocket, nickname: str):
        await ws.accept()
        self.conns[nickname] = ws
        # self.connections.append(ws)
    
    # 2. 클라이언트와 연결이 끊어졌을때
    def disconnect(self, ws: WebSocket, nickname: str):
        # self.connections.remove(ws)
        del self.conns[nickname]

    # 3. 특정 소켓에게 메세지 보내기
    async def send(self, ws: WebSocket, msg: str):
        await ws.send_text(msg)

    async def send_to(self, nickname: str, msg: str) -> bool:
        nickname = nickname.replace('@', '')
        ws = self.conns.get(nickname, None)
        if ws is None:
            return False
        await ws.send_text(msg)        

    # 4. 전체 클라이언트에게 메세지 보내기
    async def broadcast(self, msg: str):
        keys = self.conns.keys()
        for key in keys:
            ws = self.conns[key]
            await ws.send_text(msg)
        # for ws in self.connections:
        #     await ws.send_text(msg)

ws_manager = WSManager()
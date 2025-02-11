# ws_router.py
from fastapi import (
    APIRouter, WebSocket, WebSocketDisconnect
)
from fastapi.responses import HTMLResponse
from app.dependencies.ws_manager import ws_manager

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: 
            <input type="text" id="username" />
        </h2>
            <input type="button" value="connect" onclick="connect();" />
        
            <input type="text" id="messageText" autocomplete="off"/>
            <button onclick="sendMessage()">Send</button>
        <ul id='messages'>
        </ul>
        <script>
            var ws = null;
            function connect(){
                var userName = document.getElementById('username').value;
                if(userName.length < 1){
                    alert('ID를 입력해주세요.');
                    return false;
                }
                if(ws != null){
                    ws.close();
                    ws = null;
                    console.log('socket closed');
                }
                
                ws = new WebSocket(`ws://localhost:8000/ws/${userName}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
            }
            function sendMessage() {
                var input = document.getElementById("messageText")
                if(input.value.length < 1){
                    return;
                }
                ws.send(input.value)
                input.value = ''
            }
            
        </script>
    </body>
</html>
"""

@router.get('/')
def home():
    return HTMLResponse(html)

# DM 기능 있는 버전
@router.websocket('/ws/{nickname}')
async def websocket_endpoint(ws: WebSocket,
                             nickname: str):
    await ws_manager.connect(ws, nickname)
    await ws_manager.broadcast(f'{nickname} 들어옴.')
    try:
        while True:
            # @nickname 밥 먹엇 나?
            data = await ws.receive_text()
            if data.startswith('@'):
                arTokens = data.split(' ')
                targetName = None # DM받을 사용자의 닉네임
                if len(arTokens) > 1:
                    targetName = arTokens[0] # @nickname
                    msg = ' '.join(arTokens[1:]) # 밥 먹엇 나?
                    await ws_manager.send_to(targetName, f'{nickname}: {msg}')
                    continue

            await ws_manager.broadcast(f'{nickname}: {data}')
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)
        await ws_manager.broadcast(f'{nickname} 나감')

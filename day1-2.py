from socket import *
import re #정규표현식 사용을 위한 모듈
import json
from enum import Enum
from dataclasses import dataclass

class HttpContentType(Enum):
    APPLICATION_JSON = 'application/json'
    TEXT_HTML = 'text/html'
    IMAGE_PNG = 'image/png'

class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'
    PATCH = 'PATCH'

@dataclass
class HttpRequest:
    method: HttpMethod
    url: str

db = [
    {'id':1, 'name':"Trump"},
    {'id':2, 'name':"Biden"},
    {'id':3, 'name':"Kim"},
    {'id':4, 'name':"Lee"},
    {'id':5, 'name':"Park"}
]

class HttpStatusCode(Enum):
    OK = (200, 'OK')
    NOT_FOUND = (404, 'Not Found')
    SEE_OTHER = (303, 'See Other')
    SERVER_ERROR = (500, 'Internal Server Error')

def makeResponseHeader(status:HttpStatusCode,
                        contentType:HttpContentType,
                        extra: dict|None = None) -> str:
    res = f'HTTP/1.1 {status.value[0]} {status.value[1]}\n'
    res += f'Content-Type: {contentType.value}\n'
    if extra:
        for key, value in extra.items():
            res += f'{key}: {value}\n'
    res += '\n'
    return res

def parseRequest(requests:str) -> HttpRequest | None:
    if len(requests) < 1:
        return None
    arRequests = requests.split('\n')
    for line in arRequests:
        match = re.search(r'\b(GET|POST|DELETE|PUT|PATCH)\b\s+(.*?)\s+HTTP/1.1',line) # group(1) : Method, group(2) : Path
        if match:
            method=HttpMethod(match.group(1))
            url=match.group(2)
            try:
                return HttpRequest(method, url)
            except ValueError:
                return None
    return None

def get_user_from_db():
    return db

def createServer():
    arPath = ['/', '/users', '/google.png', '/google']
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080)); #포트번호 설정
        serverSocket.listen();  #서버가 클라이언트의 요청을 받을 준비
        while True:
            #클라이언트가 요청을 보내면 accept()로 연결을 수락
            (connectionSocket, addr) = serverSocket.accept(); 
            print(addr)
            #클라이언트가 보낸 메시지를 받기 위해 recv() 함수를 사용
            req = connectionSocket.recv(1024).decode('utf-8');
            httpreq = parseRequest(req)
            strPath = httpreq.url;
            if(httpreq is None or strPath is None):
                connectionSocket.shutdown(SHUT_WR)
                continue
            #응답 헤더 작성
            res = '';
            #요청한 경로가 존재하지 않을 때
            if strPath not in arPath:
                res = makeResponseHeader(HttpStatusCode.NOT_FOUND, HttpContentType.TEXT_HTML)
                res += '<html><body>404 Not Found</body></html>\n'

            elif strPath == '/users':
                users = get_user_from_db()
                res = makeResponseHeader(HttpStatusCode.OK, HttpContentType.APPLICATION_JSON)
                res += json.dumps(get_user_from_db())

            elif strPath == '/google.png':
                res = makeResponseHeader(HttpStatusCode.OK, HttpContentType.IMAGE_PNG)
                connectionSocket.sendall(res.encode('utf-8')) # 헤더 전송
                with open('google.png', 'rb') as f:
                    while chunk := f.read(1024):
                        connectionSocket.sendall(chunk)
                connectionSocket.shutdown(SHUT_WR)
                continue

            elif strPath == '/google':
                res = makeResponseHeader(HttpStatusCode.SEE_OTHER, HttpContentType.TEXT_HTML, {'Location':'https://www.google.com'})

            elif strPath == '/':
                res = makeResponseHeader(HttpStatusCode.OK, HttpContentType.TEXT_HTML)
                res += '<html><body>Hello World<br><img src="/google.png"/></body></html>\n'
            
            #클라이언트에 응답 보내기
            connectionSocket.sendall(res.encode('utf-8'))
            connectionSocket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        serverSocket.close()

if __name__ == '__main__':
    createServer()
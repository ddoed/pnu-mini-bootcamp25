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
    userAgent: str

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
    METHOD_NOT_ALLOWED = (405, 'Method Not Allowed')

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
            req = HttpRequest()
            try:
                req.method = HttpMethod(match.group(1))
                req.url = match.group(2)
            except:
                return None
            
            return req
    return None

def get_user_from_db():
    return db

def handle_req(req: HttpRequest) -> bytes:
    arPath = ['/', '/users', '/google.png', '/google']
    if req is None:
        resp = makeResponseHeader(HttpStatusCode.METHOD_NOT_ALLOWED, 
                                HttpContentType.TEXT_HTML)
        return resp.encode('utf-8')

    print(f'Path={req.url}')
    strPath = req.url
    # 고객께 답변 드리기
    bResp = bytes()
    if strPath not in arPath:
        resp = makeResponseHeader(HttpStatusCode.NOT_FOUND, 
                                HttpContentType.TEXT_HTML)
        resp += '<html><body>없습니다</body></html>\n'
        bResp = resp.encode('utf-8')

    elif strPath == '/users':
        resp = makeResponseHeader(HttpStatusCode.OK, 
                                HttpContentType.APPLICATION_JSON)
        resp += json.dumps(get_user_from_db())
        bResp = resp.encode('utf-8')

    elif strPath == '/google':
        resp = makeResponseHeader(HttpStatusCode.MOVED_PERMANENTLY, 
                                HttpContentType.TEXT_HTML, 
                                {'Location': 'https://www.google.com'})
        bResp = resp.encode('utf-8')
        
    elif strPath == '/google.png':
        resp = makeResponseHeader(HttpStatusCode.OK,
                                HttpContentType.IMAGE_PNG)
        bResp = resp.encode('utf-8')

        with open('google.png', 'rb') as f:
            bResp += f.read()
    else:
        resp = makeResponseHeader(HttpStatusCode.OK, HttpContentType.TEXT_HTML)
        resp += '<html><body>Hello <img src="/google.png" /></body></html>'
        bResp = resp.encode('utf-8')
        
    return bResp

def createServer():
    
    serverSocket = socket(AF_INET, SOCK_STREAM)
    try:
        serverSocket.bind(('localhost', 8080)); #포트번호 설정
        serverSocket.listen();  #서버가 클라이언트의 요청을 받을 준비
        while True:
            (cSocket, addr) = serverSocket.accept()
            print(addr)

            req = cSocket.recv(1024).decode('utf-8')
            print(req)
            httpReq = parseRequest(req)

            bRes = handle_req(httpReq)
            cSocket.sendall(bRes)

            cSocket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        serverSocket.close()

if __name__ == '__main__':
    createServer()
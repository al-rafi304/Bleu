import socket
from datetime import datetime, timezone
from http_objects import HTTPResponse, HTTPRequest

class TCPServer:
    def __init__(self, port:int, ip='127.0.0.1'):
        self.ip = ip
        self.port = port
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # Allows resusable sockets
        sock.bind((self.ip, self.port))
        sock.listen()
        print(f"Server listening at {self.ip}:{self.port}")
        
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            
            response = self.handle_request(data)
            conn.sendall(response.to_bytes())

            # print(f"Client conneted {addr[0]}:{addr[1]}")
            conn.close()
    
    def handle_request(self, data):
        response = HTTPResponse()
        return response.status(200).body('<h1>TCP Server running</h1>')

class HTTPServer(TCPServer):
    format = 'utf-8'
    __routes = {
        'GET': {
            '/': lambda: '<h1>Hello World</h1>'
        },
        'POST': {},
        'PUT': {},
        'DELETE': {},

    }

    def handle_request(self, data):
        req_raw = data.decode(self.format)

        response = HTTPResponse()
        request = HTTPRequest(req_raw)

        # Checking invalid requests
        if request.method not in self.__routes.keys():
            return response.status(501).body('<h1>501 Not Implemented</h1>')
        elif self.__routes[request.method].get(request.path) == None:
            return response.status(404).body('<h1>404 Not Found</h1>')
        

        return self.__routes[request.method][request.path](request, response)

    def route(self, method, path, func):
        if self.__routes.get(method) == None:
            self.route[method] = {path: func}
        else:
            self.__routes[method].update({path: func})


def mainPage(req, res):
    res.body('<center><h1>Home Page</h1></center>')
    
    return res
def testPage(req, res):
    if req.method == 'GET':
        res.body(f'<h1>Get request</h1>')
    elif req.method == 'POST':
        res.json({'test': 123, 'blabla': 1234})
    
    return res

if __name__ == '__main__':
    server = HTTPServer(port=8888)
    try:
        server.route('GET', '/', mainPage)
        server.route('GET', '/test', testPage)
        server.route('POST', '/test', testPage)
        server.start()
    except KeyboardInterrupt:
        print(' Exiting...')

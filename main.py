import socket
from datetime import datetime, timezone

class TCPServer:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8888
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # Allows resusable sockets
        sock.listen()
        print(f"Server listening at {self.ip}:{self.port}")
        
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            
            response = self.handle_request(data)
            conn.sendall(response)

            # print(f"Client conneted {addr[0]}:{addr[1]}")
            conn.close()
    
    def handle_request(self, data):
        return data

class HTTPServer(TCPServer):
    format = 'utf-8'
    headers = {
        'Server': 'BOSS',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented'
    }
    routes = {
        'GET': {
            '/': lambda: '<h1>Hello World</h1>'
        },
        'POST': {},
        'PUT': {},
        'DELETE': {},

    }

    def response_headers(self, extra=None):
        date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        if extra:
            extra.update({'Date': date})
            self.headers.update(extra)
        else:
            self.headers.update({'Date': date})

        headers = ''
        for key, value in self.headers.items():
            h = f'{key}: {value}\r\n'
            headers += h

        return headers.encode(self.format)
    
    def response_status(self, code):
        status = f'HTTP/1.1 {code} {self.status_codes[code]}\r\n'
        return status.encode(self.format)

    def handle_request(self, data):
        req_raw = data.decode(self.format)
        req_line = req_raw.split('\n')[0]
        req_method = req_line.split(' ')[0]
        req_path = req_line.split(' ')[1]

        print(req_line)

        # Checking invalid requests
        if req_method not in self.routes.keys():
            return self.HTTP_501_handler()
        elif self.routes[req_method].get(req_path) == None:
            return self.HTTP_404_handler()

        body = self.routes[req_method][req_path]()
        
        if req_method == 'GET':
            return self.HTTP_GET_handler(body=body.encode(self.format))

    def route(self, method, path, func):
        if self.routes.get(method) == None:
            self.route[method] = {path: func}
        else:
            self.routes[method].update({path: func})
    
    def HTTP_GET_handler(self, body, status=200):
        content_length = {'Content-Length': len(body)}
        status_line = self.response_status(status)
        headers = self.response_headers(content_length)

        return b"".join([status_line, headers, b'\r\n', body])
    
    def HTTP_404_handler(self):
        body = b'<h1>404 Not Found</h1>'
        content_length = {'Content-Length': len(body)}
        status_line = self.response_status(404)
        headers = self.response_headers(content_length)

        return b"".join([status_line, headers, b'\r\n', body])
    
    def HTTP_501_handler(self):
        body = b'<h1>501 Not Implemented</h1>'
        content_length = {'Content-Length': len(body)}
        status_line = self.response_status(501)
        headers = self.response_headers(content_length)

        return b"".join([status_line, headers, b'\r\n', body])


def mainPage():
    # status = 200
    body = '<center><h1>Home Page</h1></center>'
    return body
def testPage():
    # status = 200
    body = '<h1>test Page</h1>'
    return body

if __name__ == '__main__':
    server = HTTPServer()
    try:
        server.route('GET', '/', mainPage)
        server.route('GET', '/test', testPage)
        server.start()
    except KeyboardInterrupt:
        print(' Exiting...')

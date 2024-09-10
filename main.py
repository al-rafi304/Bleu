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

            print(f"Client conneted {addr[0]}:{addr[1]}")
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
    }

    def response_headers(self, extra=None):
        date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        if extra:
            extra.update({'Date': date})
            self.headers.update(extra)
        else:
            self.headers.update(date)

        headers = ''
        for key, value in self.headers.items():
            h = f'{key}: {value}\r\n'
            headers += h

        return headers.encode(self.format)
    
    def response_status(self, code):
        status = f'HTTP/1.1 {code} {self.status_codes[code]}\r\n'
        return status.encode(self.format)

    def handle_request(self, data):
        body = b'<h1>Hello World!</h1>'

        content_length = {'Content-Length': len(body)}
        status_line = self.response_status(200)
        headers = self.response_headers(content_length)

        return b"".join([status_line, headers, b'\r\n', body])

if __name__ == '__main__':
    server = HTTPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print(' Exiting...')
import socket

class TCPServer:
    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 8888
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen()
        print(f"Server listening at {self.ip}:{self.port}")
        
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            conn.sendall(data)
            print(f"Client conneted {addr[0]}:{addr[1]}")
            conn.close()

if __name__ == '__main__':
    server = TCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print(' Exiting...')
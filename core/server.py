import socket
import threading
import re
from .request import HTTPRequest
from .response import HTTPResponse

class TCPServer:
    def __init__(self, port:int, ip='127.0.0.1'):
        self.ip = ip
        self.port = port
    
    def start(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # Allows resusable sockets
            sock.bind((self.ip, self.port))
            sock.listen()
            print(f"Server listening at {self.ip}:{self.port}")
            while True:
                conn, addr = sock.accept()

                # Threading
                th = threading.Thread(target=self.handle_client, args=(conn, addr))
                th.start()
        except KeyboardInterrupt:
            print('\nServer Terminated!')
    
    def handle_client(self, conn, addr):
        data = conn.recv(1024)
        response = self.handle_request(data)
        conn.sendall(response.to_bytes())
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
        'PATCH': {}
    }
    __middlewares = []

    def handle_request(self, data):
        req_raw = data.decode(self.format)
        # print(f'---------------------Request-----------------\n{req_raw}')

        response = HTTPResponse()
        request = HTTPRequest(req_raw)

        # Checking invalid requests
        if request.method not in self.__routes.keys():
            return response.status(501).body('<h1>501 Not Implemented</h1>')

        # Resolving handler and route parameters for request
        handler, params = self.__get_handler(request.method, request.path)
        request.params = params

        # Triggering Middlewares
        for midd in self.__middlewares:
            try:
                midd(request, response)
            except Exception as e:
                print(f"Error in middleware: {e}")
                response.status(500).body("<h1>Error occurred</h1>")
                return response

        # No handler found for requested route
        if handler == None:
            return response.status(404).body('<h1>404 Not Found</h1>')
        
        # Trigger Handler
        try:
            response = handler(request, response)
        except Exception as e:
            print(f"Error in route handler: {e}")
            response.status(500).body("<h1>Error occurred</h1>")
            return response
        
        return response

    def use(self, middleware):
        if not callable(middleware):
            raise TypeError("Middleware is not a callable function!")
        self.__middlewares.append(middleware)

    def route(self, method, path, handler):
        if self.__routes.get(method) == None:
            self.route[method] = {path: handler}
        else:
            self.__routes[method].update({path: handler})

    def __get_handler(self, method, path):
        for route_path, handler in self.__routes[method].items():

            # Extract route parameters (e.g. id in :id) from the route_path
            param_names = re.findall(r':([^\/]+)', route_path)
            # Converts route path with params into regular expression
            # turns a route path like /users/:id into a regex pattern 
            # like /users/([^\/]+), which can be used to match URLs like /users/123
            route_regex = re.sub(r':[^\/]+', r'([^\/]+)', route_path)
            # adding the start (^) and end ($) anchors so that entire URL must match
            route_regex = f'^{route_regex}$'

            match = re.match(route_regex, path)
            if match:
                params_values = match.groups()
                params = dict(zip(param_names, params_values))
                return handler, params
        
        return None, {}


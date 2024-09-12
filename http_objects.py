from datetime import datetime, timezone

HTTPStatus = {
    200: 'OK',
    404: 'Not Found',
    501: 'Not Implemented'
}


class HTTPResponse:
    def __init__(self, status=200, body='', headers=None):
        self.__body = body
        self.__headers = {
        'Server': 'BOSS',
        'Content-Type': 'text/html',
        'Content-Length': len(self.__body)
        }
        self.__format = 'utf-8'
        self.__status = status

        self.add_headers(headers)
    
    def add_headers(self, extra=None):
        date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        if extra:
            extra.update({'Date': date})
            self.__headers.update(extra)
        else:
            self.__headers.update({'Date': date})
        return self

    def get_headers(self):
        headers = ''
        for key, value in self.__headers.items():
            h = f'{key}: {value}\r\n'
            headers += h
        return headers
    
    def status(self, code):
        if code not in HTTPStatus.keys():
            raise Exception(f'Status code {code} not implemented yet')
        self.__status = code
        return self

    def get_status_line(self):
        status = f'HTTP/1.1 {self.__status} {HTTPStatus[self.__status]}\r\n'
        return status
    
    def body(self, content):
        self.__body = content
        self.__headers['Content-Length'] = len(self.__body)
        return self
    
    def to_bytes(self):
        status_line = self.get_status_line().encode(self.__format)
        headers = self.get_headers().encode(self.__format)
        body = self.__body.encode(self.__format)
        return b"".join([status_line, headers, b'\r\n', body])
    
    def __str__(self):
        status_line = self.get_status_line()
        headers = self.get_headers()
        body = self.__body
        return "".join([status_line, headers, '\r\n', body])
    
class HTTPRequest:
    def __init__(self, raw_req):
        self.__raw_req = raw_req
        self.__req_line = raw_req.split('\n')[0]
        self.__method = self.__req_line.split(' ')[0]
        self.__path = self.__req_line.split(' ')[1]

        self.__headers = {}
        self.__files = []       # Needs to be implemented

        for header in self.__raw_req.split('\r\n')[1:]:
            if header == '':
                continue
            key = header.split(':')[0].replace('-', '_').upper()
            value = header.split(':')[1].strip()

            if key == 'Host':
                self.__headers[key] = value.split(':')[0]
                self.__headers['SERVER_PORT'] = value.split(':')[1]
                continue

            self.__headers[key] = value
        
    @property
    def method(self):
        return self.__method
    @property
    def path(self):
        return self.__path
    @property
    def headers(self):
        return self.__headers
    @property
    def line(self):
        return self.__req_line
    
    def __str__(self):
        return self.__raw_req

        
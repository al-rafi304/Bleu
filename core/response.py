from .cookie import Cookie
from .status import HTTPStatus
from datetime import datetime, timezone
import json

class HTTPResponse:
    def __init__(self, status=200, body=''):
        self.__body = body
        self.__headers = {
        'Server': 'BOSS',
        'Date': datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
        'Content-Type': 'text/html',
        'Content-Length': len(self.__body),
        'Connection': 'keep-alive'
        }
        self.__format = 'utf-8'
        self.__status = status
        self.cookies = Cookie()

    def set_headers(self, headers:dict):
        self.__headers.update(headers)
    
    def status(self, code):
        if code not in HTTPStatus.keys():
            raise Exception(f'Status code {code} not implemented yet')
        self.__status = code
        return self
    
    def close_connection(self):
        self.__headers['Connection'] = 'close'
        return self
    
    def body(self, content):
        self.__body = content
        self.__headers['Content-Length'] = len(self.__body)
        return self
    
    def json(self, content):
        js = json.dumps(content)
        self.__headers['Content-Type'] = 'application/json'
        self.__headers['Content-Length'] = len(js)
        self.__body = js
        return self
    
    def to_bytes(self):
        status_line = self.__formatted_status_line().encode(self.__format)
        headers = self.__formatted_headers().encode(self.__format)
        body = self.__body.encode(self.__format)
        return b"".join([status_line, headers, b'\r\n\r\n', body])

    def __formatted_headers(self):
        headers = '\r\n'.join([f'{key}: {value}' for key, value in self.__headers.items()])
        if not self.cookies.isEmpty:
            headers += '\r\n' + self.cookies.to_string()

        return headers

    def __formatted_status_line(self):
        status = f'HTTP/1.1 {self.__status} {HTTPStatus[self.__status]}\r\n'
        return status

    def __str__(self):
        status_line = self.__formatted_status_line()
        headers = self.__formatted_headers()
        body = self.__body
        return "".join([status_line, headers, '\r\n', body])
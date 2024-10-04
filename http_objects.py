from datetime import datetime, timezone
import json
from urllib.parse import unquote

HTTPStatus = {
    200: 'OK',
    404: 'Not Found',
    501: 'Not Implemented'
}


class HTTPResponse:
    def __init__(self, status=200, body='', headers=None, connection='keep-alive'):
        self.__body = body
        self.__headers = {
        'Server': 'BOSS',
        'Content-Type': 'text/html',
        'Content-Length': len(self.__body),
        'Connection': connection
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
    
    def close_connection(self):
        self.__headers['Connection'] = 'close'
        return self

    def get_status_line(self):
        status = f'HTTP/1.1 {self.__status} {HTTPStatus[self.__status]}\r\n'
        return status
    
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
        self.__path = self.__req_line.split(' ')[1].split('?')[0]
        self.__headers = self.__extract_headers()
        self.__query = self.__extract_queries()
        self.__body = self.__extract_body(raw_body=''.join(raw_req.split('\r\n\r\n')[1:]))
        self.__files = []       # Needs to be implemented

    def __extract_headers(self):
        headers = {}
        for header in self.__raw_req.split('\r\n\r\n')[0].split('\r\n')[1:]:
            if header == '':
                continue
            key = header.split(':')[0].replace('-', '_').upper()
            value = header.split(':')[1].strip()

            if key == 'Host':
                headers[key] = value.split(':')[0]
                headers['SERVER_PORT'] = value.split(':')[1]
                continue

            headers[key] = value
        return headers
    
    def __extract_queries(self):
        queries = {}
        if '?' in self.__req_line.split(' ')[1]:
            for query in self.__req_line.split(' ')[1].split('?')[1].split('&'):
                key = query.split('=')[0]
                val = query.split('=')[1]
                queries[key] = unquote(val)

        return queries
    
    # Supports: plain text, json, form-urlencoded
    def __extract_body(self, raw_body):
        body = {}
        if self.__headers.get('CONTENT_TYPE') in ['text/plain', 'application/x-www-form-urlencoded']:
            for params in raw_body.split('&'):
                key = params.split('=')[0]
                val = unquote(params.split('=')[1])
                body[key] = val
        elif self.__headers.get('CONTENT_TYPE') == 'application/json':
            body = json.loads(raw_body)
        
        return body


    @property
    def method(self):
        return self.__method
    @property
    def path(self):
        return self.__path
    @property
    def query(self):
        return self.__query
    @property
    def headers(self):
        return self.__headers
    @property
    def body(self):
        return self.__body
    @property
    def line(self):
        return self.__req_line
    
    def __str__(self):
        return self.__raw_req

        
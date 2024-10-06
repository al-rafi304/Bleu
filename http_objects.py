from datetime import datetime, timezone
import json
from urllib.parse import unquote

HTTPStatus = {
    200: 'OK',
    404: 'Not Found',
    501: 'Not Implemented'
}


class Cookie:
    def __init__(self):
        self.__cookie = {}

    def set(self, name, value, maxAge=None,expires=None,
            domain=None, path='/', httpOnly=None, sameSite='Lax', secure=None):
        
        cookie = f'Set-Cookie: {name}={value}; Path={path}'

        if maxAge:
            cookie += f'; Max-Age={maxAge}'
        if expires:
            cookie += f'; Expires={expires}'
        if domain:
            cookie += f'; Domain={domain}'
        if httpOnly:
            cookie += f'; HttpOnly'
        if secure:
            cookie += f'; Secure'

        if sameSite == None:
            cookie += '; SameSite=None'
            if not secure:
                cookie += '; Secure'
        else:
            cookie += f'; SameSite={sameSite}'
        
        
        self.__cookie[name] = cookie

    @property
    def isEmpty(self):
        if self.__cookie == {}:
            return True
        return False

    def get(self, name):
        return self.__cookie[name]
    
    def get_all(self):
        return self.__cookie
    
    def to_string(self):
        return '\r\n'.join([self.__cookie[key] for key in self.__cookie.keys()])
        

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
        self.__cookies = Cookie()

    def set_headers(self, headers:dict):
        self.__headers.update(headers)
    
    def set_cookie(self, name, value, **kwargs):
        self.__cookies.set(name, value, **kwargs)
    
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
        if not self.__cookies.isEmpty:
            headers += '\r\n' + self.__cookies.to_string()

        return headers

    def __formatted_status_line(self):
        status = f'HTTP/1.1 {self.__status} {HTTPStatus[self.__status]}\r\n'
        return status

    def __str__(self):
        status_line = self.__formatted_status_line()
        headers = self.__formatted_headers()
        body = self.__body
        return "".join([status_line, headers, '\r\n', body])
    
class HTTPRequest:
    def __init__(self, raw_req):
        self.__raw_req = raw_req
        self.__req_line = raw_req.split('\n')[0]
        self.__method = self.__req_line.split(' ')[0]
        self.__path = self.__req_line.split(' ')[1].split('?')[0]
        self.header = self.__extract_header()
        self.query = self.__extract_queries()
        self.params = {}
        self.body = self.__extract_body(raw_body=''.join(raw_req.split('\r\n\r\n')[1:]))
        self.files = []       # Needs to be implemented

    def __extract_header(self):
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
        if self.header.get('CONTENT_TYPE') in ['text/plain', 'application/x-www-form-urlencoded']:
            for params in raw_body.split('&'):
                key = params.split('=')[0]
                val = unquote(params.split('=')[1])
                body[key] = val
        elif self.header.get('CONTENT_TYPE') == 'application/json':
            body = json.loads(raw_body)
        
        return body


    @property
    def method(self):
        return self.__method
    @property
    def path(self):
        return self.__path
    @property
    def line(self):
        return self.__req_line
    
    def __str__(self):
        return self.__raw_req

        
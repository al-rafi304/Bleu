from .cookie import Cookie
import json
from urllib.parse import unquote 
    
class HTTPRequest:
    def __init__(self, raw_req):
        self.__raw_req = raw_req
        self.__req_line = raw_req.split('\n')[0]
        self.__method = self.__req_line.split(' ')[0]
        self.__path = self.__req_line.split(' ')[1].split('?')[0]
        self.header = self.__extract_header()
        self.cookies = Cookie.parse(self.header.get('COOKIE'))
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
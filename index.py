from server import HTTPServer, HTTPResponse, HTTPRequest
from time import sleep

def mainPage(req:HTTPRequest, res:HTTPResponse):
    res.body('<center><h1>Home Page</h1></center>')
    return res

def testPage(req:HTTPRequest, res:HTTPResponse):
    res.set_cookie(name='id', value='123', httpOnly=True, secure=True)
    res.set_cookie(name='name', value='rafi', httpOnly=True, secure=True)

    res.body(f'<h1>Test Page</h1>{req.path} <br>Cookies: {req.cookies} <br>Query: {req.query}')

    # print(f"Path: {req.path}\nQuery:{req.query}\nHeaders:{req.header}")
    return res

def postPage(req:HTTPRequest, res:HTTPResponse):
    print(f"Path: {req.path}\nBody: {req.body}\nQuery:{req.query}\nParams:{req.params}")
    data = {'id': 1, 'count': {'A': 3, 'B': 9}}
    return res.json(data)

def busyPage(req, res):
    sleep(5)
    return res.body("<h1>Now I'm free</h1>")

if __name__ == '__main__':
    server = HTTPServer(port=8888)
    try:
        server.route('GET', '/', mainPage)
        server.route('GET', '/test', testPage)
        server.route('POST', '/post/:id', postPage)
        server.route('GET', '/busy', busyPage)
        server.start()
    except KeyboardInterrupt:
        print(' Exiting...')
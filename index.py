from server import HTTPServer
from time import sleep

def mainPage(req, res):
    res.body('<center><h1>Home Page</h1></center>')
    return res

def testPage(req, res):
    res.body(f'<h1>Test Page</h1>')
    print(f"Path: {req.path}\nQuery:{req.query}\nHeaders:{req.header}")
    return res

def postPage(req, res):
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
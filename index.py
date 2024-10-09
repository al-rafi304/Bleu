from core.server import HTTPServer, HTTPResponse, HTTPRequest

def mainPage(req:HTTPRequest, res:HTTPResponse):
    res.body('<center><h1>Home Page</h1></center>')
    return res

def testPage(req:HTTPRequest, res:HTTPResponse):
    res.set_cookie(name='id', value='123', httpOnly=True, secure=True)
    res.set_cookie(name='name', value='rafi', httpOnly=True, secure=True)

    res.body(f'<h1>Test Page</h1>{req.path} <br>Cookies: {req.cookies} <br>Query: {req.query} <br>Params: {req.params}')

    return res

def postPage(req:HTTPRequest, res:HTTPResponse):
    print(f"Path: {req.path}\nBody: {req.body}\nQuery:{req.query}\nParams:{req.params}")
    data = {'id': 1, 'count': {'A': 3, 'B': 9}}
    return res.json(data)

# Demo for authentication middleware 
def check_auth(req, res):
    req.params['Authenticated'] = False
    username = req.query.get('username')
    password = req.query.get('password')
    if username == 'peter' and password == 'spiderman':
        req.params['Authenticated'] = True

def authorizedPage(req, res):
    if not req.params.get('Authenticated'):
        return res.status(401).body('<h1>YOU ARE NOT AUTHORIZED!!</h1>')
    return res.body("<h1>Welcome authorized user!</h1>")

if __name__ == '__main__':
    server = HTTPServer(port=8888)

    server.use(check_auth)

    server.route('GET', '/', mainPage)
    server.route('GET', '/test', testPage)
    server.route('GET', '/secret', authorizedPage)
    server.route('POST', '/post/:id', postPage)

    server.start()
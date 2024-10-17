from core.server import HTTPServer
from core.session import SessionManager

def mainPage(req, res):
    if req.isAuth:
        return res.body('<center><h1>Home Page</h1>Welcome Authenticated User!</center>')
    res.body('<center><h1>Home Page</h1></center>')
    return res

def testPage(req, res):
    res.cookies.set(name='id', value='123', httpOnly=True, secure=True)
    res.cookies.set(name='name', value='rafi', httpOnly=True, secure=True)
    
    res.body(f'<h1>Test Page</h1>{req.path} Session: {req.session.id}<br>Session Data: {req.session.data} <br>Cookies: {req.cookies} <br>Query: {req.query} <br>Params: {req.params}')
    return res

def postPage(req, res):
    print(f"Path: {req.path}\nBody: {req.body}\nQuery:{req.query}\nParams:{req.params}")
    data = {'id': 1, 'count': {'A': 3, 'B': 9}}
    return res.json(data)

def login(req, res):
    username = req.query.get('username')
    password = req.query.get('password')
    if username == 'peter' and password == 'spiderman':
        req.session['auth'] = True
        return res.body("You are logged in!")
    
    return res.body("Send credentials in 'username' & 'password' query")

def logout(req, res):
    if req.isAuth:
        req.session = req.session.destroy()
        return res.body('<center><h1>Logged Out</h1>Session destroyed!</center>')
    return res.body('You are not logged in')

# Demo for authentication middleware 
def check_auth(req, res, next):
    if req.session.get('auth') == True:
        req.isAuth = True
    else:
        req.isAuth = False
    
    return next()


if __name__ == '__main__':
    server = HTTPServer(port=8888)

    session = SessionManager()

    server.use(session.middleware)
    server.use(check_auth)

    server.route('GET', '/', mainPage)
    server.route('GET', '/test', testPage)
    server.route('POST', '/post/:id', postPage)
    server.route('GET', '/login', login)
    server.route('GET', '/logout', logout)

    server.start()
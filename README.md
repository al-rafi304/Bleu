# Intro

A Python backend framework inspired by Express.js, built to handle HTTP requests, routing, and session management with ease. Every component is made from scratch including the HTTP server and the user workflow for this framwork is similiar to Express.js.

**Note: This is not a fully fledged project and it's not supposed to be. I started this project only to learn more about HTTP and got curious how frameworks work. There are high possibilities of security vulnerabilites as of now**

## Features

- **Routing**: Supports HTTP methods like `GET`, `POST`, `PUT`, `DELETE`, and custom routes with parameters.
- **Request Handling**: Provides `HTTPRequest` and `HTTPResponse` classes to handle client requests and generate responses.
- **Route Parameters**: Easily define route parameters (e.g., `/product/:id`) and access them directly in your handler functions.
- **Query Parsing**: Automatically parses query parameters, making them accessible as part of the request object.
- **Cookie Management**: Simplified cookie handling using the `Set-Cookie` header, including options for `httpOnly`, `secure`, etc.
- **Threaded Request Handling**: Uses threading to handle multiple client connections concurrently.

## Usage

Here is an example of how to use the framework in `index.py`:
```python
from core.server import HTTPServer

# Create a new instance of HTTPServer
server = HTTPServer(port=8080)

# Define route handlers
def home(req, res):
    res.body('<h1>Welcome to MyPythonFramework!</h1>')
    return res

# Define routes 
server.route('GET', '/', home)

# Start the server
server.start()
```
```bash
$ python index.py
```

For a more detailed example, check out `index.py` in the repo.

## API Reference
### Routing
 - Defining Routes: Use `server.route(method, path, handler)` to add routes
 - Route Parameters: Define routes with parameters using the format `your/route/:param`, and access them using `req.params` in the route handler
 - Supported Methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`

### Request Object
 - `req.body`: Access request body. *Current supported content types are: `text/plain`, `application/json`, `application/x-www-form-urlencoded`*
 - `req.params`: Access route parameters.
 - `req.query`: Access query parameters.
 - `req.cookies`: Access request cookies.
 - `req.header`: Access request headers.
 - `req.method`: Returns request method.
 - `req.path`: Returns request path.

### Response Object
 - `res.body(content:str)`: Set HTML content for the response body with `String` as the content type.

    ```python
    res.body("<h1>Hello World</h1>")
    ```
 - `res.json(content:dict)`: Set JSON content for the response body with `Dict` as the content type.

    ```python
    res.json({'id': 1, 'product': {'color': 'red', 'count': 12}})
    ```
 - `res.status(code:int)`: Set HTTP status code for the response. Default status code is 200 (OK).

    ```python
    res.status(404)
    ```
 - `res.set_headers(headers:dict)`: Add more headers to the response. Default headers are, `Server`, `Date`, `Content-type`, `Content-length`, `Connection`.
    
    ```python
    res.set_headers({'Accept': 'text/html'})
    ```
 - `res.set_cookie(name, value, **kwargs)`: Set a cookie to the response with various parameters. Current supported parameters are: `maxAge`, `expires`, `domain`, `path`, `httpOnly`, `sameSite`, `secure`.
    
    ```python
    res.set_cookie(name='id', value='123' httpOnly=True, secure=True)
    ```
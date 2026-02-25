from wsgiref.simple_server import make_server
import threading

ROUTES_SIMPLE = {}
HTTP_CODES = {200: 'OK', 404: 'Not Found', 500: 'Internal Server Error'}

class Request(threading.local):
    def bind(self, environ) -> None:
        self._environ = environ
        self.path = environ.get("PATH_INFO", "/")

    @property
    def method(self) -> str:
        return self._environ.get("REQUEST_METHOD", "GET").upper()

    @property
    def query_string(self) -> str:
        return self._environ.get("QUERY_STRING", "")

class Response(threading.local):
    def bind(self):
        self.status = 200
        self.content_type = 'text/html'
        self.header = {}

def route(url, method='GET'):
    def wrapper(handler):
        ROUTES_SIMPLE.setdefault(method, {})[url] = handler
        return handler
    return wrapper

request = Request()
response = Response()

def WSGIHandler(environ, start_response):
    request.bind(environ)
    response.bind()
    path = environ.get("PATH_INFO", "/")
    handler = ROUTES_SIMPLE.get(request.method, {}).get(path)
    if handler:
        output = handler()
    else:
        response.status = 404
        output = 'Not Found'
    status = f'{response.status} {HTTP_CODES[response.status]}'
    start_response(status, [('Content-Type', response.content_type)])
    return [output.encode()]
    
@route("/index", method='GET')
def hello():
    return f"'Method': {request.method}, 'Path': {request.path}, 'Query String': {request.query_string}"

@route("/about", method='GET')
def about():
    return "This is a clone of Bottle framework"

@route("/json", method='POST')
def json_test():
    response.content_type = "application/json"
    return '{"name": "bottle"}'
    
server = make_server("localhost", 8080, WSGIHandler)
print(f"Server listening at http://localhost:8080/")
server.serve_forever()

from wsgiref.simple_server import make_server
import threading

ROUTES_SIMPLE = {}

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

def route(url):
    def wrapper(handler):
        ROUTES_SIMPLE[url] = handler
        return handler
    return wrapper

request = Request()

def WSGIHandler(environ, start_response):
    request.bind(environ)
    path = environ.get("PATH_INFO", "/")
    handler = ROUTES_SIMPLE.get(path)
    if handler:
        output = handler()
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [output.encode()]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not Found"]

@route("/index")
def hello():
    return f"'Method': {request.method}, 'Path': {request.path}, 'Query String': {request.query_string}"

@route("/about")
def about():
    return "This is a clone of Bottle framework"
    
server = make_server("localhost", 8080, WSGIHandler)
print(f"Server listening at http://localhost:8080/")
server.serve_forever()

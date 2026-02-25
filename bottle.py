from wsgiref.simple_server import make_server

ROUTES_SIMPLE = {}

def route(url):
    def wrapper(handler):
        ROUTES_SIMPLE[url] = handler
        return handler
    return wrapper

def WSGIHandler(environ, start_response):
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
    return "Hello World!"

@route("/about")
def about():
    return "This is a clone of Bottle framework"
    
server = make_server("localhost", 8080, WSGIHandler)
print(f"Server listening at http://localhost:8080/")
server.serve_forever()

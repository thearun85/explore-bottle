from wsgiref.simple_server import make_server

def WSGIHandler(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Hello World!"]

server = make_server("localhost", 8080, WSGIHandler)
print("Listening on http://localhost:8080/")
server.serve_forever()

import time
import threading

class UnsafeRequest(threading.local):
    def bind(self, environ):
        self._environ = environ
        self.path = environ.get("PATH_INFO", "/")

unsafe_request = UnsafeRequest()

def simulate_request(name, path):
    environ = {"PATH_INFO": path}
    unsafe_request.bind(environ)
    time.sleep(0.1)
    print(f"Name: {name}, Path -> {unsafe_request.path}")
    

t1 = threading.Thread(target=simulate_request, args=("Thread-1", "/thread1"))
t2 = threading.Thread(target=simulate_request, args=("Thread-2", "/thread2"))

t1.start()
t2.start()
t1.join()
t2.join()
    

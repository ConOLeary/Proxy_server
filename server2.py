# import socket programming library 
import socket
  
# import thread module 
from _thread import *
import threading 

import requests

import atexit

print_lock = threading.Lock() 

def release_port():
    socket.close()

def GET_request(url):
    response = requests.get(url)
    print('GET response: ', response.status_code)
    response = str(response)
    response_bytes = response.encode()
    return response_bytes

# thread function 
def threaded(c): 
    while True: 
  
        # data received from client 
        data = c.recv(1024) 
        if not data: 
            print('Bye') 
              
            # lock released on exit 
            print_lock.release() 
            break
        
        http_response = GET_request(data)
        print('about to send: ',http_response)
        # reverse the given string from client 
        #data = data[::-1] 
  
        # send back reversed string to client 
        #c.send(data) 
        c.send(http_response)
  
    # connection closed 
    c.close() 
  
  
def Main(): 
    host = "" 
  
    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 12348
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    atexit.register(release_port, s)
    print("socket bound to port", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
        
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,)) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main()
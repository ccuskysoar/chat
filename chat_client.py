import argparse, socket
import threading
from getpass import getpass

MAX_BYTES = 65535

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',1061))

def client():
    account=input('login：')
    password=getpass()
    log=account+'-'+password
    sock.send(log.encode())
    authentication=sock.recv(MAX_BYTES)
    print(authentication.decode())
    if authentication.decode() == 'Authentication Error!' :
       sock.close()
       return 
    th1 = threading.Thread(target=sendThreadFunc)
    th2 = threading.Thread(target=recvThreadFunc)
    threads = [th1, th2]
    for t in threads :
        t.setDaemon(True)
        t.start()
    t.join()

def sendThreadFunc():
    while True:
        try:
            myword = input()
            sock.send(myword.encode())
            if myword == 'logout':
               sock.close()
               return 
        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed!')

def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(MAX_BYTES)
            if otherword:
               print(otherword.decode())
            else :
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')

if __name__ == '__main__':
        client()


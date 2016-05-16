import argparse, socket
import threading
from getpass import getpass
import time
import string

MAX_BYTES = 65535
sendFlag = list()
sendFlag = [0]
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
            if sendFlag[0] == 1:
               try:
                  f = open(myword,'rb')
                  sock.send(myword.encode())
                  time.sleep(0.5)
                  while True:
                      data = f.read(MAX_BYTES)
                      if not data:
                         break
                      sock.send(data)
                  f.close()
                  time.sleep(0.5)
                  sock.send(b'EOF')
               except FileNotFoundError:
                  print('file not found!')
                  sock.send(b'@@@error@@@')
               sendFlag[0] = 0
            else:            
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
               if otherword.decode() == '@@@filename@@@':
                  sendFlag[0] = 1
                  print('Input the file name:')
               elif otherword.decode() == '@@@y/n@@@':
                  print('start receive file...')
                  filename = sock.recv(MAX_BYTES).decode()
                  path = '/'+filename
                  f = open(path,'wb')
                  while True:
                      data = sock.recv(MAX_BYTES)
                      if data == b'EOF':
                        print ('receive file success!')
                        break
                      f.write(data)
                  f.flush()   
                  f.close()  
               else :
                  print(otherword.decode())
            else :
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed!')

if __name__ == '__main__':
        client()


import argparse, socket
import threading

MAX_BYTES = 65535
mydict = dict()
mylist = list()
account_list = list()
account_list = ['qwer','asdf','zxcv','jason','admin']
password_list = list()
password_list = ['1111','1111','1111','1111','0000']
online_list = list()
online_list = [-1,-1,-1,-1,-1]



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',1062))
sock.listen(5)
print('Listening at', sock.getsockname())
def server():
    while True:
         connection, addr = sock.accept()
         print('Accept a new connection', connection.getsockname(), connection.fileno())
         try:
            buf = connection.recv(MAX_BYTES).decode()
            correct=login(buf,connection.fileno())
            if correct == 1:
               connection.send(b'welcome to server!')
               mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
               mythread.setDaemon(True)
               mythread.start()
            else :
               connection.send(b'Authentication Error!')
               connection.close()
         except :
            pass


def login(buf,connNumber):
    log=buf.split('-')
    for i in range(len(account_list)) :
        if log[0] == account_list[i] and log[1] == password_list[i] :
           online_list[i] = connNumber
           mydict[connNumber] = log[0]
           return 1
    return 0


def tellPerson(flag, whatToSay):
    for c in mylist:
        if c.fileno() == flag :
            try:
                c.send(whatToSay.encode())
            except:
                pass

def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
            except:
                pass

def checkPerson(person,myconnection):
    if mydict[myconnection.fileno()] == person :
       msg = 'Cannot talk to yourself!'
       myconnection.send(msg.encode())
       print(msg)
       return -1
    for i in range(len(account_list)):
        if person == account_list[i] :
           if online_list[i] != -1 :
              msg = 'Start to talk with '+ person +' !'
              myconnection.send(msg.encode())
              return online_list[i]
           else :
              msg = person+' is offline!'
              myconnection.send(msg.encode())
              print(msg)
              return -1
    msg = person + ' does not exist!'
    myconnection.send(msg.encode())
    print(msg) 
    return -1  

def subThreadIn(myconnection, connNumber):
    flag = -1
    mylist.append(myconnection)
    tellOthers(connNumber, '【系統提示：'+mydict[connNumber]+' 上線】')
    while True:
        try:
            recvedMsg = myconnection.recv(MAX_BYTES).decode()
            if recvedMsg:
               print(mydict[connNumber], ':', recvedMsg)
               if recvedMsg == 'friend list' and flag ==-1 :
                  listFriend()
               elif recvedMsg == 'talk' and flag ==-1  :
                  myconnection.send(b'talk to who?')
                  person = myconnection.recv(MAX_BYTES).decode()
                  flag=checkPerson(person,myconnection)
               elif recvedMsg == 'end talk' :
                  flag = -1
                  myconnection.send(b'End talk!')
               elif recvedMsg == 'friend add' and flag ==-1  :
                  addFriend()
               elif recvedMsg == 'friend rm' and flag ==-1  :
                  rmFriend()
               else :
                  if flag != -1 :
                     tellPerson(flag, mydict[connNumber]+' :'+recvedMsg)
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person leftgf')
            tellOthers(connNumber, '【系統提示：'+mydict[connNumber]+' 離線】')
            myconnection.close()
            return

if __name__ == '__main__':
        server()


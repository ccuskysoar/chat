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
sock.bind(('127.0.0.1',1061))
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

def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
            except:
                pass

def subThreadIn(myconnection, connNumber):
    #mydict[myconnection.fileno()] = 'test'
    mylist.append(myconnection)
    tellOthers(connNumber, '【系統提示：'+mydict[connNumber]+' 進入聊天室】')
    while True:
        try:
            recvedMsg = myconnection.recv(MAX_BYTES).decode()
            if recvedMsg:
               print(mydict[connNumber], ':', recvedMsg)
               tellOthers(connNumber, mydict[connNumber]+' :'+recvedMsg)

        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person leftgf')
            tellOthers(connNumber, '【系統提示：'+mydict[connNumber]+' 離開聊天室】')
            myconnection.close()
            return

if __name__ == '__main__':
        server()


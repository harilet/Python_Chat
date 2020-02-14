#Server side program
import socket;
from threading import *

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
p=input("Enter port number:")
s.bind(('172.20.3.64',p))
s.listen(3)
c,d=s.accept()
print d

global f
f=0

def send():
	global f
	while(True):
		data=raw_input()
		c.send(data)
		if data=="stop" or f==1:
			f=1
			break;

def recv():
	global f
	while(True):
		data=c.recv(1024)
		print data
		if data=="stop"  or f==1:
			f=1
			break;	
t1=Thread(target=send)
t2=Thread(target=recv)

t1.start()
t2.start()

t1.join()
t2.join()

c.close()
s.close()

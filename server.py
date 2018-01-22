
import socket
import sys
import threading 
class Client:
    
    
    def __init__(self,conn,ip,port,status,data):
         self.ip=ip
         self.port=port
         self.status="waiting"
         self.conn=conn
         self.data=data
         self.count=5
         
    
    

    
def startgame(c1,c2):
	print(c1.ip)
	print(c2.ip)
	t1 = threading.Thread(target=getdata(c1))
	t2 = threading.Thread(target=getdata(c2))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print (c1.data)
	print (c2.data)
	gameover=1;
	turn=1;
	while gameover!=0:
		if turn==1:
			c1.conn.send('attack')
			response = c1.conn.recv(1024)
			x,y=response.strip().split(' ')
			coor = int(x)*10 + int(y)
			if c2.data[coor]=='1':
				c2.count=c2.count-1
				mes = str(c2.count)
				c1.conn.send(mes)
			else:
				turn = (turn +1)%2
		else:
			c2.conn.send('attack')
			response = c2.conn.recv(1024)
			x,y=response.strip().split(' ')
			coor = int(x)*10+int(y)
			if c1.data[coor]=='1':
				c1.count=c1.count-1
				mes = str(c1.count)
				c2.conn.send(mes)
			else:
				turn = (turn +1)%2
    
		if c1.count==0 or c2.count==0:
			gameover =0;
	if c1.count==0:
		c2.conn.send('win')
		c1.conn.send('lose')
	else:
		c1.conn.send('win')
		c2.conn.send('lose')
def getdata(player):
    
    data = player.conn.recv(1024)
    '''while data!="":
        data=player.conn.recv(1024)
        if data!=" ":
            break'''
    player.data=data
    return 
port = 12345
backlog =0
maxsize = 512


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0',port))

server.listen(0)
x=0;
while True:
    (p1conn, (ip,port))= server.accept()
    x+=1
    print("client {} connected".format(x))
    client1 = Client(p1conn,ip,port,"waiting","")
    
    #print p1conn.recv(4096)
    (p2conn, (ip,port))= server.accept()
    x+=1
    print("client {} connected".format(x))
    client2 = Client(p2conn,ip,port,"waiting","")
    p1conn.send('ready')
    p2conn.send('ready')
    newthread = threading.Thread(target=startgame(client1,client2))
    newthread.start()
''' 
    

import socket               
import pickle
# next create a socket object
s = socket.socket()         
print "Socket successfully created"
 

port = 12345               
 

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))        
print "socket binded to %s" %(port)
 

s.listen(5)     
print "socket is listening"           
 

while True:
 
  
   c, addr = s.accept()     
   print 'Got connection from', addr
 
   
   data= c.recv(4096)
   print data
  
   
   c.close()
'''

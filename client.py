import socket
import string
import pickle

host = '172.16.16.179'
port = 12345
BUFFER_SIZE = 2048

cli = socket.socket()
cli.connect((host,port))

def print_board(board,x,y,al,cnt):
	if al=='h':
		for i in range(y,y+cnt):
			board[x][i]=1
	if al=='v':
		for i in range(x,x+cnt):
			board[i][y]=1
	for i in range(10):
		s=" "
		for j in range(10):
			s+= str(board[i][j])+" "
		print (s)
	return board

def SendToServer(board):
	buf=""
	for i in range(10):
		for j in range(10):
			buf+=str(board[i][j])
	#print buf
	cli.send(buf)

def sendCords():
	attack=cli.recv(512)
	if attack=="attack":
		print attack
		print ("Enter Coordinates: ")
		print()
		s = raw_input()
		cli.send(s)
	elif attack=="win" or attack=="lose":		
		print ("you {} the game".format(attack))
		exit()
def CountOfOpponent():
	count = cli.recv(512)
	print count
	if count=="0":
		print ("You Win the game")
		exit()
	else:
		print count

def Validate_Input(x,y,al,cnt,board):
	if (x<0 or x>9) or (y<0 or y>9):
		return 0
	if (al=='h' and (x+cnt)>10) or (al=='v' and (y+cnt)>10):
		return 0
	if al=='h':
		for i in range(x,x+cnt):
			if board[x][i]==1:
				return 1
		return 2
	elif al=='v':
		for i in range(y,y+cnt):
			if board[i][y]==1:
				return 1
		return 2
		
ships = {"Aircraft Carrier":5,
		     "Battleship":4,
 		     "Submarine":2,
		     "Destroyer":3,
		     "Patrol Boat":1}
print ships			 

cnt = 5

board= []
for i in range(10):
	board_row = []
	mark_row = []
	for j in range(10):
		board_row.append(0)
		
	board.append(board_row)
	

waiting= "Waiting for opponent"
print waiting

ready= cli.recv(512)

if ready=="ready":
	for _ in range(5):
		print "Enter starting coordinates and v or h"
		f=0
		while (f!=1):
			x,y,al=raw_input().split(' ')
			var = Validate_Input(int(x),int(y),al,cnt,board)
			if(var==0):
				print "Enter Valid Input"
			if(var==1):
				print "Ship is already there enter another input"
			else:
				f=1
		print x,y,al
		board = print_board(board,int(x),int(y),al,cnt)
		cnt-=1
	#print board
	SendToServer(board)
	while True:
		sendCords()
		CountOfOpponent()
#cli.send(buf)
cli.close()
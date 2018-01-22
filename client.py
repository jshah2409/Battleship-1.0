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
	for j in range(10):
		board_row.append(0)
	board.append(board_row)

waiting= "Waiting for opponent"
print waiting

ready= cli.recv(512)

if ready=="ready":
	for _ in range(5):
		print "Enter starting coordinates and v or h"
		x,y,al=raw_input().split(' ')
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
#!/usr/bin/python3



import	socket
import	time

from	settings		import	*

import	client_tools	as 		tools
from	client_tools	import	console

import	geth


addressString = "0xea45041a6f49d1b4551861c9379fd7c475d22909"
enodeString = "enode://993d81a284a7579d2716c2efb0dbed1724208fcdd8e854ccfb552eab2f418e4b88a6cd6b658ef7aa6ca4b3db2d48ef395bc66528f2ffcf8c7a0bbef624064f39@127.0.0.1:30303"



def send_byte(b):
	s.send(b)

def send_int(i):
	s.send(i.to_bytes(1,byteorder='big'))

def send_text(t):
	s.send(t.encode('UTF-8'))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tsap_server = ('localhost',30302)
s.connect(tsap_server)
print("connected")


send_byte(CC__START)
send_byte(CC__RECIEVE_ENODE)
send_int(len(enodeString))
send_text(enodeString)

send_byte(CC__REQUEST_PEERS_ENODE)
nb = int.from_bytes(s.recv(CC_LEN_OF_SIZE), byteorder='big')
print("  nb : " + str(nb))
for i in range(nb):
	size = int.from_bytes(s.recv(CC_LEN_OF_SIZE), byteorder='big')
	enode = s.recv(size).decode('UTF-8')
	print("enode : " + enode)

while 1:
	time.sleep(5)
	send_byte(CC__PING)

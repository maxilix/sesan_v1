#!/usr/bin/python3



import	socket
import	time

import	geth
import	utils
from	utils		import	console
from	settings	import	* 



addressString = "0xea45041a6f49d1b4551861c9379fd7c475d22909"
enodeString = "enode://993d81a284a7579d2716c2efb0dbed1724208fcdd8e854ccfb552eab2f418e4b88a6cd6b658ef7aa6ca4b3db2d48ef395bc66528f2ffcf8c7a0bbef624064f39@132.210.82.28:30303"



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
send_byte(CC__SEND_ENODE)
send_int(len(enodeString))
send_text(enodeString)

time.sleep(5)
send_byte(CC__PING)
time.sleep(5)
send_byte(CC__SEND_ADDRESS)
send_int(len(addressString))
send_text(addressString)

while 1:
	send_byte(CC__PING)
	time.sleep(5)


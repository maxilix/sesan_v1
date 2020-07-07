#!/usr/bin/python3



import socket
import geth
import utils

estr = "enode://993d81a284a7579d2716c2efb0dbed1724208fcdd8e854ccfb552eab2f418e4b88a6cd6b658ef7aa6ca4b3db2d48ef395bc66528f2ffcf8c7a0bbef624064f39@132.210.82.28:30303"


def send_byte(b = 0):
	s.send(b.to_bytes(1,byteorder='big'))

def send_text(t=""):
	s.send(t.encode('UTF-8'))



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tsap_server = ('localhost',30302)

s.connect(tsap_server)
print("connected")

#(bEnode, bIp, bPort) = geth.enode_to_bytes(estr)


#init
send_byte(0)

#s.send(bEnode)
#s.send(bPort)
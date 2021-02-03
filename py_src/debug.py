import	json
import	server
import	threading
import 	math
import 	hashlib


from	settings		import	*

import	geth

import	server_managment
import	server_contract
import	server_console

import	server_tools	as 		tools
from	server_tools	import	console


#################################   DEBUG   ####################
def rm(contract):
	if (contract == "eigenTrust"):
		tools.eigenTrust = {}
	if (contract == "PoRX"):
		tools.PoRX = {}
	if (contract == "IM"):
		tools.interventionManager = []



def deploy():
	rm("eigenTrust")
	geth.unlock_coinbase(3600)
	server_console.mine(1)
	server_contract.deploy_eigenTrust()


def sha(a,b):
	aBytes = a.to_bytes(32, byteorder='big', signed=False)
	bBytes = b.to_bytes(32, byteorder='big', signed=False)
	return aBytes + bBytes

################################################################

def hhh(nonce):
	nonceBytes = nonce.to_bytes(32, byteorder='big', signed=False)
	headerBytes = tools.PoRX.functions.previous_header().call()
	return hashlib.sha256(headerBytes + nonceBytes).digest()


def mmm(g):
	s = tools.PoRX.functions.self_threshold().call()
	b = tools.w3.eth.blockNumber
	nonce = 0
	while (hhh(nonce)>s):
		if (b != tools.w3.eth.blockNumber):
			print("out")
			return
		nonce += 1
	tools.PoRX.functions.self_submit(nonce).transact({'gas':g})
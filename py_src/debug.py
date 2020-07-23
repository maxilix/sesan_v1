import	json
import	server
import	threading


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
	rm("PoRX")
	geth.unlock_coinbase(3600)
	server_console.mine(1)
	server_contract.deploy_PoRX()




################################################################


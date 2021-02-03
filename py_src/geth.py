
import	os
import	time
import	subprocess
import	json
from	web3			import	Web3 , IPCProvider
from	web3.middleware import	geth_poa_middleware


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console


"""
def enode_to_bytes(enodeString):
	bEnode = int(enodeString.split('@')[0][8:],16).to_bytes(64, byteorder='big')
	bIp = bytes([int(enodeString.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)])
	bPort = int(enodeString.split('@')[1].split(':')[1]).to_bytes(2, byteorder='big')
	return (bEnode, bIp, bPort)


def bytes_to_enode(bEnode, bIp, bPort):
	r = "enode://"
	r+= "{0:x}".format(int.from_bytes(bEnode, byteorder='big'))
	r+= "@"
	for i in bIp:
		r+= str(i)
		r+= "."
	r = r[:-1] + ":"
	r+= str(int.from_bytes(bPort, byteorder='big'))
	return r
"""



##################################################################################################
#	
#
#
def run_geth_node(nodeName):
	proc = subprocess.Popen("geth --datadir ./eth_{0}/ --networkid {1} --port {2} {3} 2> ./eth_{0}/{4} &".format(nodeName,tools.conf["geth"]["networkid"],tools.conf["geth"]["port"],"".join(["--"+flag+" " for flag in tools.conf["geth"]["flags"]]),LOG_GETH_FILENAME), shell=True, stdout=subprocess.PIPE)
	#kill sh process
	subprocess.run("kill {0}".format(proc.pid), shell=True, stdout=subprocess.PIPE)
	console(LOG_FLAG_INFO, "geth is running")
##################################################################################################


def IPC_geth_connection(nodeName):
	global provider

	console(LOG_FLAG_INFO, "waiting IPC connection ...")
	while not os.path.exists("./eth_{0}/geth.ipc".format(nodeName)):
		time.sleep(1)
	time.sleep(1)

	provider = Web3.IPCProvider("./eth_{0}/geth.ipc".format(nodeName))
	tools.w3 = Web3(provider)
	tools.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
	if (tools.w3.isConnected()):
		console(LOG_FLAG_INFO, "IPC connection successful to {0} geth node".format(nodeName))
	else:
		console(LOG_FLAG_ERROR, "IPC connection failed")

	return




def check_coinbase():
	try:
		print("coinbase : " + tools.w3.eth.coinbase)
	except ValueError:
		console(LOG_FLAG_ERROR, "coinbase not initialized.")

	if (tools.w3.eth.coinbase != tools.conf["geth"]["coinbase"]):
		console(LOG_FLAG_ERROR, "coinbase doesn't match with conf file")

	set_default_account(tools.w3.eth.coinbase)
	
	t = 3
	while t>0:
		try:
			tools.coinbasePassword = input("password : ")
			unlock_coinbase(10)
		except ValueError:
			t-=1	
			console(LOG_FLAG_WARN, "wrong password, {} try left".format(t))
			continue

		console(LOG_FLAG_INFO, "valid password")
		lock_coinbase()

		return
	console(LOG_FLAG_ERROR, "exit after 3 tests")




def set_default_account(address):
	if (address[:2] != "0x" or not tools.w3.isAddress(address)):
		console(LOG_FLAG_WARN, "eth.defaultAccount need valid address, eth.defaultAccount not set")
		return False
	else:
		tools.w3.eth.defaultAccount = address
		console(LOG_FLAG_INFO, "eth.defaultAccount set to {}".format(address))
		return True





##################################################################################################
# lock and unlock account fonction
#
#

def unlock_coinbase(secondes):
	tools.w3.geth.personal.unlock_account(tools.w3.eth.coinbase,tools.coinbasePassword,secondes)
	console(LOG_FLAG_INFO, "coinbase account unlock")

def lock_coinbase():
	tools.w3.geth.personal.lock_account(tools.w3.eth.coinbase)
	console(LOG_FLAG_INFO, "coinbase account lock")
##################################################################################################


##################################################################################################
# clique engine methodes
#
def clique_get_period():
	try:
		return clique_get_period.period
	except:
		genesidFile = open("./" + GENESIS_FILENAME , 'r')
		genesisDict = json.load(genesidFile)
		clique_get_period.period = genesisDict["config"]["clique"]["period"]
		genesidFile.close()
		return clique_get_period.period

def clique_get_signers():
	response = provider.make_request(method = "clique_getSigners", params = [])
	if ("error" in response.keys()):
		print(response)
		raise NameError("Bad RPC request")
	return response["result"]

def clique_get_proposals():
	response = provider.make_request(method = "clique_proposals", params = [])
	if ("error" in response.keys()):
		print(response)
		raise NameError("Bad RPC request")
	return response["result"]

def clique_propose(address,vote):
	if (address[:2] != "0x" or not tools.w3.isAddress(address)):
		console(LOG_FLAG_WARN, "clique engine need valid address, propose not set")
		return False
	if (type(vote)!=bool):
		console(LOG_FLAG_WARN, "clique engine need boolean vote, propose not set")
		return False

	response = provider.make_request(method = "clique_propose", params = [address,vote])
	if ("error" in response.keys()):
		print(response)
		raise NameError("Bad RPC request")
	return (response["result"] == None and clique_get_proposals()[address] == vote)

def clique_discard(address):
	if (address[:2] != "0x" or not tools.w3.isAddress(address)):
		console(LOG_FLAG_WARN, "clique engine need valid address, discard not set")
		return False

	response = provider.make_request(method = "clique_discard", params = [address])
	if ("error" in response.keys()):
		print(response)
		raise NameError("Bad RPC request")
	return (response["result"] == None and address not in clique_get_proposals())

##################################################################################################

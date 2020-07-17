
import	threading
import	random
import	math
import	json

from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console

import	server_managment


def command_selctor(cmd):
	switcher = {
		# 0 system
		CC__STOP							: lambda:connexion_exit(),
		CC__PING							: lambda:ping(),
		CC__PONG							: lambda:pong(),

		# 1 recieve
		CC__RECIEVE_ENODE					: lambda:recieve_enode(),
		CC__RECIEVE_ADDRESS					: lambda:recieve_address(),

		# 2 user request
		CC__REQUEST_SERVER_ENODE			: lambda:request_server_enode(),
		CC__REQUEST_PEERS_ENODE				: lambda:request_peers_enode(),
		CC__REQUEST_SERVER_ADDRESS			: lambda:request_server_address(),
		CC__REQUEST_PEERS_ADDRESS			: lambda:request_peers_address(),
		CC__REQUEST_CONTRACT_IM				: lambda:request_contract_intervention_manager(),
		CC__REQUEST_CONTRACT_EIGENTRUST		: lambda:request_contract_eigenTrust(),
		CC__REQUEST_NETWORKID				: lambda:request_networkid(),
		CC__REQUEST_ETHER 					: lambda:request_ether()
	}
	function=switcher.get(cmd,lambda : unknown_command())
	if ((cmd != CC__PING and cmd != CC__PONG) or tools.verbosity >= 6):
		console(LOG_FLAG_CC, "opCode received : 0x{:02x}".format(ord(cmd)))
	tools.clients[threading.currentThread().name]["timestamp"] = tools.now()
	return function()


def unknown_command():
	console(LOG_FLAG_WARN, "unknown command, ignored")







################################################################
#################################   SYSTEM   ###################
#CC__START							0x00


#CC__STOP							0x00
def connexion_exit():
	server_managment.close_self_connexion("connexion closed by client")


#CC__PING							0x01
def ping():
	tools.clients[threading.currentThread().name]["socket"].send(CC__PONG)


#CC__PONG							0x02
def pong():
	if(tools.verbosity >= 6):
		console(LOG_FLAG_CC,"pong reply")






################################################################
#################################   RECIEVE   ##################

#CC__RECIEVE_ENODE					0x10
def recieve_enode():
	currentClient = tools.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size == 0):
		server_managment.close_self_connexion("size of enode must be nonzero")
		return
	currentClient["enodeString"] = currentClient["socket"].recv(size).decode('UTF-8')
	currentClient["update"] = C_UPDATE_PEERABLE
	console(LOG_FLAG_CC, "enode received : {}...".format(currentClient["enodeString"][:32]))


#CC__RECIEVE_ADDRESS				0x11
def recieve_address():
	currentClient = tools.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size != 42):
		server_managment.close_self_connexion("size of address must be 42 (not a joke :D)")
		return
	currentClient["addressString"] = currentClient["socket"].recv(size).decode('UTF-8')
	currentClient["update"] = C_UPDATE_ADDRESS
	console(LOG_FLAG_CC, "address received : {}".format(currentClient["addressString"]))






################################################################
#################################   USER REQUEST   #############

#CC__REQUEST_SERVER_ENODE			0x20
def request_server_enode():
	currentClient = tools.clients[threading.currentThread().name]
	enodeBytes = tools.w3.geth.admin.node_info()["enode"].encode('UTF-8')
	size = len(enodeBytes)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(enodeBytes)
	console(LOG_FLAG_CC, "server enode sent")


#CC__REQUEST_PEERS_ENODE			0x21
def request_peers_enode():
	currentClient = tools.clients[threading.currentThread().name]
	peerableClient = [c for c in tools.clients if (tools.clients[c]["peerable"] and tools.clients[c]!=currentClient)]
	enodeNumber = math.ceil(len(peerableClient)*GETH_PERCENT_PEER_ENODE_SENT/100)
	if (enodeNumber == 0):
		console(LOG_FLAG_WARN,"no client peerable, server enode is sending")
		currentClient["socket"].send(int(1).to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		request_server_enode()
		return
	enodeNumber = min(enodeNumber,GETH_MAX_PEER_ENODE_SENT)
	enodeToSend = []
	while (len(enodeToSend)<enodeNumber):
		enodeToSend.append(tools.clients[random.choice(peerableClient)]["enodeString"])
	currentClient["socket"].send(enodeNumber.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	for enodeString in enodeToSend:
		enodeBytes = enodeString.encode('UTF-8')
		currentClient["socket"].send(len(enodeBytes).to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		currentClient["socket"].send(enodeBytes)
	console(LOG_FLAG_CC, "{} peers enode sent".format(enodeNumber))


#CC__REQUEST_SERVER_ADDRESS			0x22
def request_server_address():
	# WHY	
	console(LOG_FLAG_WARN, "why client want server address ???")
	"""currentClient = tools.clients[threading.currentThread().name]
	addressBytes = tools.w3.eth.coinbase.encode('UTF-8')
	size = len(addressBytes)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(addressBytes.encode('UTF-8'))
	console(LOG_FLAG_CC, "server address sent")"""


#CC__REQUEST_PEERS_ADDRESS			0x23
def request_peers_address():
	# WHY
	console(LOG_FLAG_WARN, "why client want peers address ???")
	#currentClient = tools.clients[threading.currentThread().name]



#CC__REQUEST_CONTRACT_IM			0x24
def request_contract_intervention_manager():
	currentClient = tools.clients[threading.currentThread().name]
	contractNumber = len(tools.interventionManager)
	currentClient["socket"].send(contractNumber.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	"""
	for contract in tools.interventionManager:
		addressBytes = contract["address"].encode('UTF-8')
		size = len(addressBytes)
		currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		currentClient["socket"].send(addressBytes)
		abiBytes = json.dump(contract["abi"]).encode('UTF-8')
		size = len(abiBytes)
		currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		currentClient["socket"].send(abiBytes)"""


#CC__REQUEST_CONTRACT_EIGENTRUST	0x25
def request_contract_eigenTrust():
	currentClient = tools.clients[threading.currentThread().name]
	if (tools.eingenTrust == None):
		console(LOG_FLAG_WARN, "no deployed eigenTrust contract")
		currentClient["socket"].send(int(0).to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		return
	"""
	addressBytes = tools.eingenTrust["address"].encode('UTF-8')
	size = len(addressBytes)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(addressBytes)
	abiBytes = json.dump(tools.eingenTrust["abi"]).encode('UTF-8')
	size = len(abiBytes)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(abiBytes)"""


#CC__REQUEST_NETWORKID				0x26
def request_networkid():
	currentClient = tools.clients[threading.currentThread().name]
	if (tools.w3.geth.admin.node_info().protocols.eth.network != tools.conf["geth"]["networkid"]):
		console(LOG_FLAG_ERROR, "networkid doesn't match with conf file")
	currentClient["socket"].send(tools.conf["geth"]["networkid"].to_bytes(CC_LEN_OF_SIZE, byteorder='big'))


#CC__REQUEST_ETHER					0x27
def request_ether():
	currentClient = tools.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	weiRequest = int.from_bytes(currentClient["socket"].recv(size), byteorder='big')
	console(LOG_FLAG_INFO, "client want {} wei".format(weiRequest))
	currentClient["socket"].send(CC__REQUEST_ETHER_AKW)


################################################################
#################################   AUTHENTIFICATION   #########
#CC__SERVER_COMMITMENT				0x30
#CC__SERVER_ASSO_LOGIN				0x31
#CC__SERVER_PRO_LOGIN				0x32
#CC__SERVER_HEALT_LOGIN				0x33

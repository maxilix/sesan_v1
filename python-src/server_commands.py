
import	threading
import	random
import	math

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

		# 1 sending
		CC__RECIEVE_ENODE					: lambda:recieve_enode(),
		CC__RECIEVE_ADDRESS					: lambda:recieve_address(),

		# 2 user request
		CC__REQUEST_SERVER_ENODE			: lambda:request_server_enode(),
		CC__REQUEST_PEERS_ENODE				: lambda:request_peers_enode(),
		CC__REQUEST_SERVER_ADDRESS			: lambda:console(LOG_FLAG_CC,""),
		CC__REQUEST_PEERS_ADDRESS			: lambda:console(LOG_FLAG_CC,""),
		CC__REQUEST_CONTRACT_GI				: lambda:console(LOG_FLAG_CC,""),
		CC__REQUEST_CONTRACT_EIGENTRUST		: lambda:console(LOG_FLAG_CC,""),
		CC__REQUEST_NETWORKID				: lambda:console(LOG_FLAG_CC,"")
	}
	function=switcher.get(cmd,lambda : unknown_command())
	if ((cmd != CC__PING and cmd != CC__PONG) or tools.verbosity >= 6):
		console(LOG_FLAG_CC, "opCode received : 0x{:02x}".format(ord(cmd)))
	tools.clients[threading.currentThread().name]["timestamp"] = tools.now()
	return function()


def unknown_command():
	console(LOG_FLAG_WARN, "unknown command, ignored")










# CC__STOP
def connexion_exit():
	server_managment.close_self_connexion("connexion closed by client")
	return 1



# CC__PING
def ping():
	tools.clients[threading.currentThread().name]["socket"].send(CC__PONG)


# CC__PONG
def ping():
	if(tools.verbosity >= 6):
		console(LOG_FLAG_CC,"pong reply")




# CC__RECIEVE_ENODE
def recieve_enode():
	currentClient = tools.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size == 0):
		server_managment.close_self_connexion("size of enode must be nonzero")
		return 1 
	currentClient["enodeString"] = currentClient["socket"].recv(size).decode('UTF-8')
	currentClient["update"] = C_UPDATE_PEERABLE
	console(LOG_FLAG_CC, "enode received : {}...".format(currentClient["enodeString"][:32]))
	return 0


# CC__RECIEVE_ADDRESS
def recieve_address():
	currentClient = tools.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size != 42):
		server_managment.close_self_connexion("size of address must be 42 (not a joke :D)")
		return 1
	currentClient["addressString"] = currentClient["socket"].recv(size).decode('UTF-8')
	currentClient["update"] = C_UPDATE_ADDRESS

	console(LOG_FLAG_CC, "address received : {}".format(currentClient["addressString"]))
	return 0



# CC__REQUEST_ENODE_SERVER
def request_server_enode():
	currentClient = tools.clients[threading.currentThread().name]
	enodeString = tools.w3.geth.admin.node_info()["enode"]
	size = len(enodeString)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(enodeString.encode('UTF-8'))
	console(LOG_FLAG_CC, "server enode sent")


# CC__REQUEST_ENODE_PEERS
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
	for e in enodeToSend:
		currentClient["socket"].send(len(e).to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
		currentClient["socket"].send(e.encode('UTF-8'))
	console(LOG_FLAG_CC, "{} peers enode sent".format(enodeNumber))






# CC__REQUEST_ADDRESS_SERVER
def request_server_address():
	# WHY
	currentClient = tools.clients[threading.currentThread().name]
	address = tools.w3.eth.coinbase
	size = len(enodeString)
	currentClient["socket"].send(size.to_bytes(CC_LEN_OF_SIZE, byteorder='big'))
	currentClient["socket"].send(enodeString.encode('UTF-8'))
	console(LOG_FLAG_CC, "server enode sent")


# CC__REQUEST_ADDRESS_PEERS
#def request_peers_address():
	# WHY

#CC__REQUEST_CONTRACT_GI

#CC__REQUEST_CONTRACT_EIGENTRUST

#CC__REQUEST_NETWORKID





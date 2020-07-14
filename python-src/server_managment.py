import	time
import	socket
import	threading
import	re


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console

import	geth
import	server_commands



def unknown_command():
	console(LOG_FLAG_WARN, "unknown command, ignored")


def close_client_connexion(message = ""):
	if (threading.currentThread() == threading.main_thread()):
		raise NameError("MainThread can't close connexion")

	if (message == ""):
		console(LOG_FLAG_INFO, "connexion closed")
	else:
		console(LOG_FLAG_INFO, "connexion closed : {}".format(message))

	currentClient = tools.clients.pop(threading.currentThread().name)
	currentClient["socket"].close()


def init_new_client_database(connexion,tsap):
	index = 0
	while index in [tools.clients[c]["id"] for c in tools.clients]:
		index += 1
	tools.clients[threading.currentThread().name] = dict()
	currentClient = tools.clients[threading.currentThread().name]
	currentClient["update"] = 0
	currentClient["id"] = index
	currentClient["socket"] = connexion
	currentClient["timestamp"] = tools.now()
	currentClient["ip"] = [int(tsap[0].split('.')[x]) for x in range(4)]
	currentClient["pyPort"] = tsap[1]
	#currentClient["gethPort"] = None
	currentClient["enodeString"] = None
	currentClient["addressString"] = None
	currentClient["isValidAddress"] = False
	currentClient["peerable"] = False

	console(LOG_FLAG_INFO, "new client : database initialized")



def client_database_update():
	currentClient = tools.clients[threading.currentThread().name]

	if (currentClient["update"]&C_UPDATE_ADDRESS != 0):
		currentClient["isValidAddress"] = tools.w3.isAddress(currentClient["addressString"])
		if (currentClient["isValidAddress"]):
			console(LOG_FLAG_INFO, "valid address updated")
		else:
			console(LOG_FLAG_WARN, "invalid address")
			#server_managment.close_client_connexion("address received is not valid")

	if (currentClient["update"]&C_UPDATE_PEERABLE != 0):
		enode = currentClient["enodeString"]

		#check valid enode with geth !!!!!!!!!
		if (enode[:8] != "enode://"):
			console(LOG_FLAG_WARN, "invalid enode : doesn't start with \"enode://\"")
			currentClient["peerable"] = False
		elif (enode[136] != "@"):
			console(LOG_FLAG_WARN, "invalid enode : 136th char must be '@'")
			currentClient["peerable"] = False
		elif bool(re.compile(r'[^0-9a-f]').search(enode[8:136])):
			console(LOG_FLAG_WARN, "invalid enode : public key must be hex string")
			currentClient["peerable"] = False
		elif ([int(enode.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)] != currentClient["ip"]):
			console(LOG_FLAG_WARN, "invalid enode : ip doesn't match")
			currentClient["peerable"] = False
		else:
			console(LOG_FLAG_INFO, "valid enode")
			currentClient["peerable"] = True

	currentClient["update"] = C_NO_UPDATE









def command_selctor(cmd):
	switcher = {
		# 0 system
		CC__STOP							: lambda:server_commands.connexion_exit(),
		CC__PING							: lambda:server_commands.ping(),
		CC__PONG							: lambda:console(LOG_FLAG_CC,"pong reply"),

		# 1 sending
		CC__RECIEVE_ENODE					: lambda:server_commands.recieve_enode(),
		CC__RECIEVE_ADDRESS					: lambda:server_commands.recieve_address(),

		# 2 user request
		CC__REQUEST_SERVER_ENODE			: lambda:server_commands.request_server_enode(),
		CC__REQUEST_PEERS_ENODE				: lambda:server_commands.request_peers_enode(),
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





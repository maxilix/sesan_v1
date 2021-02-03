import	time
import	socket
import	threading
import	re


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console

import	geth
import	server_commands
import	server






def close_self_connexion(message = ""):
	if (threading.currentThread() == threading.main_thread()):
		raise NameError("MainThread can't close self connexion")

	if close_connexion(threading.currentThread().name):
		if (message == ""):
			console(LOG_FLAG_INFO, "connexion closed")
		else:
			console(LOG_FLAG_INFO, "connexion closed : {}".format(message))
	
	
def close_all_connexion():
	console(LOG_FLAG_INFO, "close all connexion")
	temp = []
	for c in tools.clients:
		temp.append(c)
	for c in temp:
		close_connexion(c)



def close_connexion(h):
	currentClient = tools.clients.get(h,False)
	if not currentClient:
		#console(LOG_FLAG_WARN,"client {}...{} doesn't exist".format(h[:4],h[-4:]))
		return False
	else:
		tools.clients.pop(h)
		currentClient["socket"].close()
		return True



def client_match(hashOrId):
	match = []
	if(type(hashOrId) == str): # by hash
		for c in tools.clients:
			if (hashOrId == c[:len(hashOrId)]):
				match.append(c)
	elif(type(hashOrId) == int): # by id
		for c in tools.clients:
			if hashOrId == tools.clients[c]["id"]:
				match.append(c)
	else:
		print("use hash string or integer identifier in argument")
		return -1
	return match



def enable_server():
	"""
	check
	"""
	serverThread = threading.Thread(target=server.start_server, name="serverThread", args=( ))
	serverThread.start()


def disable_server():
	"""
	check
	"""
	tools.exit_thread("serverThread")




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













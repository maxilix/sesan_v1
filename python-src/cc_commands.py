
import	threading



import	utils
from	utils		import	console
import	server
from	settings	import	* 





# CC__STOP
def connexion_exit():
	server.close_client_connexion("connexion closed by client")
	return 1


# CC__PING
def ping():
	utils.clients[threading.currentThread().name]["timestamp"] = utils.now()
	utils.clients[threading.currentThread().name]["socket"].send(CC__PONG)



# CC__SEND_ENODE
def send_enode():
	currentClient = utils.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size == 0):
		server.close_client_connexion("size of enode must be nonzero")
		return 1 
	currentClient["enodeString"] = currentClient["socket"].recv(size).decode('UTF-8')
	console(1, "enode received : {}...".format(currentClient["enodeString"][:32]))
	return 0


def send_address():
	currentClient = utils.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size != 42):
		server.close_client_connexion("size of address must be 42 (not a joke :D)")
		return 1
	currentClient["addressString"] = currentClient["socket"].recv(size).decode('UTF-8')
	currentClient["isValidAddress"] = utils.w3.isAddress(currentClient["addressString"])
	if (not currentClient["isValidAddress"]):
		server.close_client_connexion("address received is not valid")
		return 1
	console(1, "valid address received : {}".format(currentClient["addressString"]))
	return 0

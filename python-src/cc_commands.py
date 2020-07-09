
import	threading



import	utils
from	utils		import	console
import	server
from	settings	import	* 





# CC__STOP
def connexion_exit():
	server.close_client_connexion("connexion closed by client")
	return 1


# CC__SEND_ENODE
def send_enode():
	currentClient = utils.clients[threading.currentThread().name]
	size = int.from_bytes(currentClient["socket"].recv(CC_LEN_OF_SIZE), byteorder='big')
	if (size == 0):
		server.close_client_connexion("size of enode must be nonzero")
		return 1 
	currentClient = utils.clients[threading.currentThread().name]
	currentClient["enodeString"] = currentClient["socket"].recv(size).decode('UTF-8')
	console(1, "enode cerceived : {}".format(currentClient["enodeString"]))
	return 0

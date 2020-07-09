
import	time
import	datetime
import	socket
import	threading


from	settings	import	*
import	utils
from	utils		import	console
import	geth
import	cc_commands
import	interpretor


def close_client_connexion(message):
	if (threading.currentThread() == threading.main_thread()):
		raise NameError("MainThread can't close connexion")

	console(1, "connexion closed : {}".format(message))
	client = utils.clients.pop(threading.currentThread().name)
	client["socket"].close()



def connexion_lost():
	close_client_connexion("connexion lost")



def command_selctor(cmd):
	switcher = {
		# 0 system
		CC__STOP					: lambda:cc_commands.connexion_exit(),

		# 1 sending
		CC__SEND_ENODE				: lambda:cc_commands.send_enode(),

		#
	}
	function=switcher.get(cmd,lambda : console(2, "unknowncommand, ignored"))
	return function()






def waiting_client():
	# accept new connexion
	try:
		connexion,tsap_client = utils.serverSocket.accept()
	except socket.timeout:
		return
	# rename the current tread
	threading.currentThread().name = utils.hash(str(tsap_client))

	# initialized client database
	utils.clients[threading.currentThread().name] = dict()
	currentClient = utils.clients[threading.currentThread().name]

	# set first argurments
	currentClient["socket"] = connexion
	currentClient["ip"] = [int(tsap_client[0].split('.')[x]) for x in range(4)]
	currentClient["pyPort"] = tsap_client[1]
	currentClient["timeStamp"] = datetime.datetime.now()

	console(1, "client database initialized")

	connexion.settimeout(CC_TIMEOUT)
	if (connexion.recv(1) != CC__START):
		close_client_connexion("no start opCode")
		return
	console(1, "start opCode OK : New client")

	try :
		while 1:
			cmd = None
			cmd = connexion.recv(1)
			if (cmd == None or cmd == b''):
				connexion_lost()
				return

			console(1, "command received : 0x{:02x}".format(ord(cmd)))
			if(command_selctor(cmd)): # if communication error and/or closed connexion
				return

		raise NameError("Inaccessible code line in waiting_client()")

	except socket.timeout:
		close_client_connexion("ping or reply timeout")
		return


	
	



def start_server():
	utils.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	utils.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	utils.serverSocket.bind(('',SERVER_LISTEN_PORT))
	utils.serverSocket.listen(1)
	utils.serverSocket.settimeout(1)

	console(1, "server started, listen on {0}".format(SERVER_LISTEN_PORT))

	interpretorThread = threading.Thread(target=interpretor.start_command_interpretor, name="interpretor", args=( ))
	interpretorThread.start()

	nbClient = -1

	while 1:

		newThread = threading.Thread(target=waiting_client , name="newClient" , args=( ))
		newThread.start()
		if (nbClient != len(utils.clients)):
			nbClient = len(utils.clients)
			console(1, "active client : {}".format(nbClient))

		while (newThread.is_alive() and newThread.name == "newClient"):
			if (not interpretorThread.is_alive()):
				newThread.join()
				utils.secure_exit()
			time.sleep(0.1)
		
	raise NameError("Inaccessible code line in start_server()")

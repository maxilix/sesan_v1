
import	time
import	socket
import	threading


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console

import	geth
import	server_managment
import	server_commands
import	server_contract




def client_manager():
	# accept new connexion
	try:
		connexion,tsap_client = tools.serverSocket.accept()
	except socket.timeout:
		return
	# rename the current tread
	threading.currentThread().name = tools.hash(str(tsap_client))

	# initialized client database
	server_managment.init_new_client_database(connexion,tsap_client)

	connexion.settimeout(CC_TIMEOUT)
	if (connexion.recv(1) != CC__START):
		server_managment.close_self_connexion("no start opCode") ##################CLOSE
		return
	console(LOG_FLAG_INFO, "start opCode OK : New client")


	try :
		while 1:
			cmd = None
			cmd = connexion.recv(1)
			if (cmd == None or cmd == b''):
				server_managment.close_self_connexion("connexion lost")##################CLOSE
				return

			server_commands.command_selctor(cmd)
			server_managment.client_database_update()

		raise NameError("Inaccessible code line in waiting_client()")




	except socket.timeout:
		server_managment.close_self_connexion("ping or pong reply timeout")##################CLOSE
		return
	except ConnectionResetError:
		server_managment.close_self_connexion("connexion reset failed")##################CLOSE
		return
	except OSError:
		server_managment.close_self_connexion("console command")##################CLOSE
		return

	
	



def start_server():
	tools.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tools.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tools.serverSocket.bind(('',tools.conf["server"]["port"]))
	tools.serverSocket.listen(1)
	tools.serverSocket.settimeout(1)

	console(LOG_FLAG_INFO, "server started, listen on {0}".format(tools.conf["server"]["port"]))

	#server_contract.init_contracts()
	#console(LOG_FLAG_INFO, "contract system initialized")

	nbClient = -1

	while threading.currentThread().name != "exit":

		newThread = threading.Thread(target=client_manager , name="newClient" , args=( ), daemon=True)
		newThread.start()
		if (nbClient != len(tools.clients)):
			nbClient = len(tools.clients)
			console(LOG_FLAG_INFO, "active client : {}".format(nbClient))

		while (newThread.is_alive() and newThread.name == "newClient"):
			time.sleep(0.1)

	threading.currentThread().name = "serverThread"

	server_managment.close_all_connexion()
	console(LOG_FLAG_INFO,"all client connexion closed")
	tools.serverSocket.close()

	console(LOG_FLAG_INFO, "server stopped")

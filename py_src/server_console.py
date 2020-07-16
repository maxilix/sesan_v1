import	json
import	server
import	threading


from	settings		import	*

import	server_managment
#import	server_contract

import	server_tools	as 		tools
from	server_tools	import	console


#################################   SYSTEM   ###################



def exit():
	comfirm = (input("please use secure_exit() [y/n] : ") == "y")
	if comfirm:
		tools.secure_exit()




################################################################



#################################   DISPLAY   ##################
def help():
	print("not implement")


def print_configuration():
	print(json.dumps(tools.conf, indent=2))


def print_clients(hashOrId = None, full=False):
	if (hashOrId != None):
		clients = server_managment.client_match(hashOrId)
		if (clients == -1):
			print("aborted")
			return
	else:
		clients = tools.clients

	if (len(clients) == 0):
		print("void")
		return
	for c in clients:
		print(c)
		print("\tid                " + str(tools.clients[c]["id"]))
		if (full):
			print("\tsocket            " + str(tools.clients[c]["socket"]))
		else:
			print("\tsocket            " + str(tools.clients[c]["socket"])[:64] + "...")
		print("\ttimestamp         " + str(tools.clients[c]["timestamp"]))			
		print("\tip                " + "".join(str(x)+'.' for x in tools.clients[c]["ip"])[:-1])
		print("\tpyPort            " + str(tools.clients[c]["pyPort"]))
#		print("\tgethPort          " + str(tools.clients[c]["gethPort"]))
		if (full):
			print("\tenodeString       " + str(tools.clients[c]["enodeString"]))
		else:
			print("\tenodeString       " + str(tools.clients[c]["enodeString"])[:64] + "...")
		print("\tpeerable          " + str(tools.clients[c]["peerable"]))
		print("\taddressString     " + str(tools.clients[c]["addressString"]))
		print("\tisValidAddress    " + str(tools.clients[c]["isValidAddress"]))
		print()
	print()

################################################################





#################################   SERVER   ###################

def close_client_connexion(hashOrId = None):
	clients = server_managment.client_match(hashOrId)
	if (clients == -1):
		return

	if (len(clients)==0):
		print("no client match")
		return

	print("{0} client{1} match".format(len(clients) , ("","s")[len(clients)>=2] ))
	for c in clients:
		print("\t" + c)
	confirm = input("comfirm close [y/n] : ") == "y"
	if (confirm):
		for c in clients:
			server_managment.close_connexion(c)
	else:
		print("aborted")



def server(status):
	if type(status) != bool:
		print("bool value needed")
		print("aborted")
		return

	if (status):
		for t in threading.enumerate():
			if t.name == "serverThread":
				print("server already started")
				return
		server_managment.enable_server()
	else:
		for t in threading.enumerate():
			if t.name == "serverThread":
				server_managment.disable_server()
				return
		print("server already stopped")




################################################################



#################################   TOOLS   ####################


def change_verbosity(newVerbosity):
	if (newVerbosity>=0 and newVerbosity<=6):
		tools.verbosity = v
	else:
		print("aborted")

################################################################



print("Welcome to the server management console")
print("- Use help() to see informations")
print("- Use 'tail -f ./eth_{0}/{1}' in an other terminal to see server log".format(tools.nodeName,LOG_SERVER_FILENAME))
print("- Use 'tail -f ./eth_{0}/{1}' in an other terminal to see geth log".format(tools.nodeName,LOG_GETH_FILENAME))
print("- Use 'geth --datadir ./eth_{0}/ attach' in an other terminal to use JS console".format(tools.nodeName))
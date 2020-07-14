
from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console


def exit():
	comfirm = (input("please use secure_exit() [y/n] : ") == "y")
	if comfirm:
		tools.secure_exit()



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




def print_clients(hashOrId = None, full=False):
	if (hashOrId != None):
		clients = client_match(hashOrId)
		if (clients == -1):
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




def close_client_connexion(hashOrId = None):
	clients = client_match(hashOrId)
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
			#tools.clients.pop(e[0])
			tools.clients[c]["socket"].close()
	else:
		print("aborted")









print("Welcome to the server management console")
print("- Use help() to see informations")
print("- Use 'tail -f log' in an other terminal to see log's server")
print("- Use 'geth --datadir ./eth_{}/ attach' in an other terminal to use JS console".format(tools.nodeName))
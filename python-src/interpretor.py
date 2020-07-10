
import	utils
from	utils		import	console
from	settings	import	*





def print_clients(i=None, full=False):
	if (len(utils.clients) == 0):
		print("void")
		return
	for c in utils.clients:
		if (i==None or i == c[:len(i)]):
			print(c)
			print("\tsocket            " + str(utils.clients[c]["socket"])[:64] + "...")
			print("\ttimestamp         " + str(utils.clients[c]["timestamp"]))			
			print("\tip                " + "".join(str(x)+'.' for x in utils.clients[c]["ip"])[:-1])
			print("\tpyPort            " + str(utils.clients[c]["pyPort"]))
			print("\tgethPort          " + str(utils.clients[c]["gethPort"]))
			print("\tenodeString       " + str(utils.clients[c]["enodeString"])[:64] + "...")
			print("\taddressString     " + str(utils.clients[c]["addressString"]))
			print("\tisValidAddress    " + str(utils.clients[c]["isValidAddress"]))
			print()




def close_client_connexion_by_hash(h):
	l = []
	for c in utils.clients:
		if (h == c[:len(h)]):
			l.append((c,utils.clients[c]["socket"]))
	if (len(l)==0):
		print("no client match")
		return
	else:
		print("{} clients match".format(len(l)))
		for e in l:
			print("\t" + e[0])
		confirm = input("comfirm close [yes] : ")
		if (confirm == "yes"):
			for e in l:
				#utils.clients.pop(e[0])
				e[1].close()
		else:
			print("aborted")













def command_interpretor():

	while 1:
		cmd = input().split(" ")

		# EXIT
		if (cmd[0] == CMD__EXIT and len(cmd) == 1):
			break;

		# PRINT CLIENTs LIST
		elif (cmd[0] == CMD__CLIENT_LIST and len(cmd) <= 2):
			if (len(cmd) == 1):
				print_clients()
			elif (cmd[1] == "full"):
				print_clients(full=True)
			else:
				print("\tcommand not found")

		# PRINT FILTER CLIENTS LIST
		elif (cmd[0] == CMD__CLIENT_I and len(cmd) >= 2 and len(cmd) <= 3):
			if (len(cmd) == 2):
				print_clients(cmd[1])
			elif (cmd[2] == "full"):
				print_clients(cmd[1],True)
			else:
				print("\tcommand not found")

		# CLOSE FILTER CLIENTS CONNEXION
		elif (cmd[0] == CMD__CLOSE_CLIENT_CONNEXION and len(cmd) == 2):
			close_client_connexion_by_hash(cmd[1])



		else:
			print("\tcommand not found")

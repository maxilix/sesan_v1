
import	os
import	time

from	settings	import * 
import	utils
import	geth
import	server



# relative path ./eth-{0}/ used, not home !!!!!
# geth pid failed, and so not killed !!!!!!!!!!


def main():

	utils.init()


	print("Welcome to Sesan Blochain Client.\n")
	nodeName = input("Node name : ") or DEBUG_DEFAULT_NODENAME

	if not os.path.exists("./eth-{0}".format(nodeName)):
		print("Node not initialized. Please initialize it with main_init.py")
		utils.secure_exit()

	utils.gethPid = geth.run_geth_node(nodeName)

	w3 = geth.IPC_geth_connection(nodeName)

	server.start_server(w3)


	utils.secure_exit()





###########################################################################################


main()

import	os
import	time

from	settings	import	*
import	utils
from	utils		import	console
import	geth
import	server



# relative path ./eth-{0}/ used, not home !!!!!
# geth pid failed, and so not killed !!!!!!!!!!


def main():

	utils.init()


	print("Welcome to Sesan Blochain Client.\n")
	nodeName = DEBUG_DEFAULT_NODENAME #input("Node name : ") or DEBUG_DEFAULT_NODENAME

	if not os.path.exists("./eth-{0}".format(nodeName)):
		console(3, "Node not initialized. Please initialize it with main_init.py")

	geth.run_geth_node(nodeName)

	geth.IPC_geth_connection(nodeName)

	server.start_server()


	utils.secure_exit()





###########################################################################################


main()
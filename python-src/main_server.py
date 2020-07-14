
import	os
import	time
import	threading
import	re


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console

import	geth
import	server



# relative path ./eth_{0}/ used, not home !!!!!
# dict access via .get(key,defaultIfNotKey)





def main():
	tools.init()
	tools.verbosity = DEFAULT_VERBOSITY

	print("Welcome to Sesan Blochain Client.\n")

	tools.nodeName = "."
	while (bool(re.compile(r'[^a-z]').search(tools.nodeName))):
		tools.nodeName = input("Node name (ascii lowercase lettre only)(a-z) : ") or DEFAULT_NODE_NAME
	#tools.nodeName = DEFAULT_NODE_NAME
	print("Node name : " + tools.nodeName)

	if not os.path.exists("./eth_{0}".format(tools.nodeName)):
		console(LOG_FLAG_ERROR, "Node not initialized. Please initialize it with main_init_user.py")

	geth.run_geth_node(tools.nodeName)

	geth.IPC_geth_connection(tools.nodeName)

	geth.check_coinbase()



	serverThread = threading.Thread(target=server.start_server, name="serverThread", args=( ))
	serverThread.start()



###########################################################################################


main()

from 	server_console 	import *
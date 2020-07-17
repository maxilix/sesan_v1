
import	os
import	time
import	threading
import	re


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console
import	server_contract

import	geth
import	server



# relative path ./eth_{0}/ used, not home !!!!!

# dict access via .get(key,defaultIfNotKey)

# size = len(string)
# send(size)
# send(string.encode)
# WARN len(string) may be different that len(string.encode)

# raise noblocking, use console(LOG_FLAG_ERROR) for blocking error





def main():

	print("Welcome to Sesan Blochain Client.\n")

	tempNodeName = "."
	while (bool(re.compile(r'[^a-z]').search(tempNodeName))):
		tempNodeName = input("Node name (ascii lowercase lettre only)(a-z) : ") or DEFAULT_NODE_NAME
	#tempNodeName = DEFAULT_NODE_NAME
	print("Node name : " + tempNodeName)

	if not os.path.exists("./eth_{0}".format(tempNodeName)):
		console(LOG_FLAG_ERROR, "Node not initialized. Please initialize it with main_init_user.py")
	

	tools.init(tempNodeName)



	geth.run_geth_node(tools.nodeName)

	geth.IPC_geth_connection(tools.nodeName)

	geth.check_coinbase()
	
	server_contract.init_contracts()




###########################################################################################


main()

from 	server_console 	import *
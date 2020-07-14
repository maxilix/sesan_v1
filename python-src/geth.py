
import	os
import	time
import	subprocess
from	web3		import	Web3


from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console


"""
def enode_to_bytes(enodeString):
	bEnode = int(enodeString.split('@')[0][8:],16).to_bytes(64, byteorder='big')
	bIp = bytes([int(enodeString.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)])
	bPort = int(enodeString.split('@')[1].split(':')[1]).to_bytes(2, byteorder='big')
	return (bEnode, bIp, bPort)


def bytes_to_enode(bEnode, bIp, bPort):
	r = "enode://"
	r+= "{0:x}".format(int.from_bytes(bEnode, byteorder='big'))
	r+= "@"
	for i in bIp:
		r+= str(i)
		r+= "."
	r = r[:-1] + ":"
	r+= str(int.from_bytes(bPort, byteorder='big'))
	return r
"""
	
def run_geth_node(nodeName):

	proc = subprocess.Popen("geth --nousb --datadir ./eth_{0}/ --nodiscover --networkid {1} 2> /dev/null &".format(nodeName,GETH_NETWORKID), shell=True, stdout=subprocess.PIPE)

	#kill sh process
	subprocess.run("kill {0}".format(proc.pid), shell=True, stdout=subprocess.PIPE)

	"""# geth pid
	proc = subprocess.Popen("ps -ef | grep geth", shell=True, stdout=subprocess.PIPE)
	pid = proc.communicate()[0].decode('UTF-8').split('\n')[0].split(' ')[1:]
	if (pid[0] == ""):
		pid = pid[1:]
	pid = int(pid[0])
	console(1, "Geth is running : {0}".format(pid))"""

	console(LOG_FLAG_INFO, "geth is running")
	return



def IPC_geth_connection(nodeName):

	console(LOG_FLAG_INFO, "waiting IPC connection ...")
	while not os.path.exists("./eth_{0}/geth.ipc".format(nodeName)):
		time.sleep(1)
	time.sleep(1)

	tools.w3 = Web3(Web3.IPCProvider("./eth_{0}/geth.ipc".format(nodeName)))
	if (tools.w3.isConnected()):
		console(LOG_FLAG_INFO, "IPC connection successful to {0} geth node".format(nodeName))
	else:
		console(LOG_FLAG_ERROR, "IPC connection failed")

	return




def check_coinbase():
	t = 3
	while t>0:
		try:
			print("coinbase : " + tools.w3.eth.coinbase.lower())
			tools.coinbasePassword = input("password : ")
		except ValueError:
			console(LOG_FLAG_ERROR, "coinbase not initialized.")

		try:
			unlock_coinbase(10)
		except ValueError:
			t-=1	
			console(LOG_FLAG_WARN, "wrong password, {} try left".format(t))
			continue

		console(LOG_FLAG_INFO, "valid password")
		lock_coinbase()
		return
	console(LOG_FLAG_ERROR, "exit after 3 tests")



def unlock_coinbase(secondes):
	tools.w3.geth.personal.unlock_account(tools.w3.eth.coinbase,tools.coinbasePassword,secondes)
	console(LOG_FLAG_INFO, "coinbase account unlock")


def lock_coinbase():
	tools.w3.geth.personal.lock_account(tools.w3.eth.coinbase)
	console(LOG_FLAG_INFO, "coinbase account lock")

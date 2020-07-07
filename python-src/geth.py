
import	os
import	time
import	subprocess
from	web3		import	Web3


from	settings	import	* 
import	utils


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


def run_geth_node(nodeName):

	proc = subprocess.Popen("geth --nousb --datadir ./eth-{0}/ --nodiscover --networkid {1} 2> /dev/null &".format(nodeName,GETH_NETWORKID), shell=True, stdout=subprocess.PIPE)

	#kill sh process
	subprocess.run("kill {0}".format(proc.pid), shell=True, stdout=subprocess.PIPE)

	# geth pid
	proc = subprocess.Popen("ps -ef | grep geth", shell=True, stdout=subprocess.PIPE)
	pid = proc.communicate()[0].decode('UTF-8').split('\n')[0].split(' ')[1:]
	if (pid[0] == ""):
		pid = pid[1:]
	pid = int(pid[0])
	print("Geth is running : " + str(pid))
	return pid


def IPC_geth_connection(nodeName):

	print("Waiting IPC connection.", end='')
	while not os.path.exists("./eth-{0}/geth.ipc".format(nodeName)):
		print(".",end='')
		time.sleep(1)
	print()
	time.sleep(1)

	w3 = Web3(Web3.IPCProvider("./eth-{0}/geth.ipc".format(nodeName)))
	if (w3.isConnected()):
		print("IPC connection successful to {0} geth node.".format(nodeName))
	else:
		print("IPC connection failed")
		utils.secure_exit()
	
	return w3



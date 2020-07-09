
import	os
import	sys
import	hashlib
import	threading
import	psutil


from	settings	import * 





def init():
	
	global clients
	global w3
	global serverSocket

	clients = dict()


def secure_exit():

	console(0,"secure exit")

	for proc in psutil.process_iter(['pid', 'name']):
		if (proc.info["name"] == "geth"):
			os.kill(proc.info["pid"],15)
			break
	console(0,"secure exit - geth client killed")


	for c in clients:
		clients[c]["socket"].close()
	console(0,"secure exit - all client connexion closed")

	serverSocket.close()
	console(0,"secure exit - server stoped")

	exit()


def hash(string, methode = "sha256"):
	if (methode == "sha256"):
		return hashlib.sha256(string.encode()).hexdigest()
	else:
		raise NameError("Hash methode unknown")
		return



"""MainThread"""

def console(flags, message, fd = sys.stdout):

	error = False

	# FLAGS
	if   (flags == LOG_FLAG_INFO):
		print(" [INFO] ", file=fd, end = '')
	elif (flags == LOG_FLAG_WARNING):
		print(" [WARN] ", file=fd, end = '')
	elif (flags == LOG_FLAG_ERROR):
		print("[ERROR] ", file=fd, end = '')
		error = True
	else:
		print("        ", file=fd, end = '')

	# CLIENT or SYSTEM
	if (threading.currentThread() == threading.main_thread()):
		print("   SYSTEM   : " , file=fd, end = '')
	else:
		print(threading.currentThread().name[:4] + "..." + threading.currentThread().name[-4:] + " : ", file=fd, end = '')
	# MESSAGE
	print(message)

	if error:
		secure_exit()



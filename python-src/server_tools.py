import	psutil
import	os
import	threading
import	hashlib
import	datetime


from	settings	import	* 


def init():

	global nodeName
	global w3
	global logFile
	global verbosity
	global coinbasePassword
	global clients
	global serverSocket
	clients = dict()
	logFile = open(LOG_PATHFILE,'w')



def hash(string, methode = "sha256"):
	if (methode == "sha256"):
		return hashlib.sha256(string.encode()).hexdigest()
	else:
		raise NameError("Hash methode unknown")
		return



def now():
	return datetime.datetime.now()



def console(flag, message, fd = LOG_PATHFILE, who = None):
	error = (flag == LOG_FLAG_ERROR)
	if (flag<=verbosity):

		if (fd == LOG_PATHFILE):
			fd = logFile

		# flag
		if   (flag == LOG_FLAG_SECURE_EXIT):
			fd.write(" [EXIT] ")
		elif (flag == LOG_FLAG_ERROR):
			fd.write("\033[31m[ERROR] \033[0m")
		elif (flag == LOG_FLAG_WARN):
			fd.write("\033[33m [WARN] \033[0m")
		elif (flag == LOG_FLAG_INFO):
			fd.write("\033[32m [INFO] \033[0m")
		elif (flag == LOG_FLAG_NOFLAG):
			fd.write("        ")
		elif (flag == LOG_FLAG_CC):
			fd.write("\033[34m  [CMD] \033[0m")
		else:
			raise NameError("Flag no supported")

		# who
		if (who != None):
			if(len(who)>11):
				raise NameError("'who' max length is 11 in console()")
			fd.write(who.join(" " for i in range(11-len(who))) + " : ")
		elif (threading.currentThread() == threading.main_thread()):
			fd.write("Console     : ")
		elif (threading.currentThread().name == "serverThread"):
			fd.write("Server sys  : ")
		else:
			fd.write(threading.currentThread().name[:4] + "..." + threading.currentThread().name[-4:] + " : ")

		# massage
		fd.write(message + "\n")
		fd.flush()

	if error:
		secure_exit()



def secure_exit():

	console(LOG_FLAG_SECURE_EXIT,"secure exit")

	for proc in psutil.process_iter(['pid', 'name']):
		if (proc.info["name"] == "geth"):
			os.kill(proc.info["pid"],15)
			break
	console(LOG_FLAG_SECURE_EXIT,"geth client killed")

	if (len(clients)>0):
		console(LOG_FLAG_SECURE_EXIT,"{0} client{1} connected".format(len(clients),("","s")[len(clients)>=2]))
		for c in clients:
			clients[c]["socket"].close()
		console(LOG_FLAG_SECURE_EXIT,"all client connexion closed")

	for t in threading.enumerate():
		if t.name == "serverThread":
			t.name = "exit"

	console(LOG_FLAG_SECURE_EXIT,"server is stopping")

	logFile.close()
	exit()

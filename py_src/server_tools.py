import	psutil
import	os
import	threading
import	hashlib
import	datetime
import	json


from	settings	import	*



def init(tempNodeName):

	global nodeName
	nodeName = tempNodeName

	global conf
	with open("./eth_{0}/{1}".format(nodeName,CONFIG_FILENAME),'r') as fd:
		conf = json.load(fd)

	global w3

	global logFile
	logFile = open("./eth_{0}/{1}".format(nodeName,LOG_SERVER_FILENAME),'w')

	global verbosity
	verbosity = conf.get("verbosity",DEFAULT_VERBOSITY)

	global coinbasePassword

	global clients
	clients = dict()

	global serverSocket

	global eigenTrust
	eigenTrust = {}

	global PoRX
	PoRX = {}

	global interventionManager
	interventionManager = []







def hash(string, methode = "sha256"):
	if (methode == "sha256"):
		return hashlib.sha256(string.encode()).hexdigest()
	else:
		raise NameError("Hash methode unknown")
		return



def now():
	return datetime.datetime.now()



def console(flag, message, fd = LOG, who = None):
	error = (flag == LOG_FLAG_ERROR)
	if (flag<=verbosity):

		if   (fd == LOG):
			fd = logFile
		elif (fd == STDOUT):
			fd = sys.stdout
		elif (fd == STDERR):
			fd = sys.stderr
		else:
			raise NameError("file descriptor not supported")


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
			fd.write("\033[34m [CMD]  \033[0m")
		else:
			raise NameError("Flag no supported")

		# who
		if (who != None):
			if(len(who)>11):
				raise NameError("'who' max length is 11 in console()")
			fd.write(who)
			fd.write("".join(" " for i in range(11-len(who))))
			fd.write(" : ")
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



def exit_thread(threadName):
	for t in threading.enumerate():
		if t.name == threadName:
			t.name = "exit"
			t.join()



def secure_exit():

	console(LOG_FLAG_SECURE_EXIT,"secure exit")


	exit_thread("serverThread")

	exit_thread("eigenTrustSpyThread")
	exit_thread("PoRXSpyThread")


	for proc in psutil.process_iter(['pid', 'name']):
		if (proc.info["name"] == "geth"):
			os.kill(proc.info["pid"],15)
			break
	console(LOG_FLAG_SECURE_EXIT,"geth client killed")
	"""
	if (len(clients)>0):
		console(LOG_FLAG_SECURE_EXIT,"{0} client{1} connected".format(len(clients),("","s")[len(clients)>=2]))
		import	server_managment
		server_managment.close_all_connexion()
		del server_managment
	console(LOG_FLAG_SECURE_EXIT,"all client connexion closed")
	"""


	with open("./eth_{0}/{1}".format(nodeName,CONFIG_FILENAME),'w') as fd:
		json.dump(conf, fd, sort_keys=True, indent=2)
	console(LOG_FLAG_SECURE_EXIT,"configuration file saved")

	logFile.close()
	exit()


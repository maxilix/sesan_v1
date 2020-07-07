
import os
import signal

from	settings	import * 





def init():
	global gethPid
	global clients
	clients = dict()
	log.file = open(LOG_PATHFILE, "w")


def secure_exit():

	print("SECURE EXIT")

	log.file.close()
	#os.kill(gethPid, signal.SIGSTOP)
	exit()







def log(flags, client, message):
	# FLAGS
	if (flags >= LOG_FLAG_ERROR):
		flags -= LOG_FLAG_ERROR
		log.file.write("[ERROR] ")
	if (flags >= LOG_FLAG_WARNING):
		flags -= LOG_FLAG_WARNING
		log.file.write("[WARN]  ")
	if (flags >= LOG_FLAG_INFO):
		flags -= LOG_FLAG_INFO
		log.file.write("[INFO]  ")

	# CLIENT or SYSTEM
	if (client == None):
		#				(255.255.255.255 , 65536)
		log.file.write("(        system         )  ")
	else:
		log.file.write(str(client[3]+"  "))

	# MESSAGE
	log.file.write(str(message) + "\n")


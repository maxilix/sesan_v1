
import	time
import	datetime
#import	queue
import	socket
import	threading


from	settings	import * 
import	utils
import	geth


def close_client_connexion(connexion, message):
	print("client " + str(threading.currentThread().name))
	print("client connexion closed : " + message)
	utils.clients.pop(threading.currentThread().name)
	connexion.close()
	threading.currentThread().stop()









def waiting_client(s, w3):

	connexion,tsap_client = s.accept()
	if (connexion.recv(1) != CC_BALISE_START):
		#log
		connexion.close()
		print("Not 0x00 to initialized. connexion closed.")
		return
	print("0x00 OK : New client")
	connexion.settimeout(CC_TIMEOUT)

	threading.currentThread().name = utils.hash(str(tsap_client))
	utils.clients[threading.currentThread().name] = dict()
	currentClient = utils.clients[threading.currentThread().name]
	currentClient["timeStamp"] = datetime.datetime.now()
	#log
	print(threading.currentThread().name + " initialized")

	try :
		while 1:
			cmd = connexion.recv(1)

			print("foret d'iff")
			if (cmd == CC_BALISE_STOP):
				close_client_connexion(connexion, "0x00 OK")
				break
			if (cmd == CC_BALISE_SEND_ENODE): # CS enodeString
				print("0x10 send enode")
				size = int.from_bytes(connexion.recv(CC_LEN_OF_SIZE), byteorder='big')
				print("size of enode in byte : " + str(size))
				currentClient["enodeString"] = connexion.recv(size).decode('UTF-8')
		

		print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx")

	except socket.timeout:
		close_client_connexion(connexion, "PING or reply timeout")

	
	



def start_server(w3):
	print("main thread :")
	print(threading.currentThread())
	print(threading.currentThread().name())

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('',30302))
	s.listen(1)

	while 1:
		#newFIFO = queue.Queue()
		newThread = threading.Thread(target=waiting_client , name="newClient" , args=(s, w3, ))
		newThread.start()
		while (newThread.name == "newClient"):
			time.sleep(0.1)
		
		#break
		#if (newFIFO.get() == b'\x00'):
			#                  queue     thread       connexion      tsap_client
		#	clients.append( ( newFIFO , newThread , newFIFO.get() , newFIFO.get() ) )
		#print("New connexion initialized" + str(clients[len(clients)-1][3]))
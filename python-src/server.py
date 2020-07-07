
import	time
import	datetime
#import	queue
import	socket
import	threading
import	hashlib


from	settings	import * 
import	utils
import	geth







def waiting_client(s, w3):

	connexion,tsap_client = s.accept()
	if (connexion.recv(1) != CC_BALISE_START):
		#log
		connexion.close()
		print("Not 0x00 to initialized. connexion closed.")
		return
	print("0x00 OK : New client")
	connexion.settimeout(2)

	threading.currentThread().name = hashlib.sha256(str(tsap_client).encode()).hexdigest()
	utils.clients[threading.currentThread().name] = dict()
	currentClient = utils.clients[threading.currentThread().name]
	currentClient["timeStamp"] = datetime.datetime.now()
	#log
	print(threading.currentThread().name + " initialized")

	while 1:
		cmd = None
		try:
			cmd = connexion.recv(1)
		except socket.timeout:
			print("timeout")
			continue


		print("foret d'iff")
		if (cmd == CC_BALISE_STOP):
			print("0x00 OK : close connexion")
			utils.clients.pop(threading.currentThread().name)
			connexion.close()
			break
		if (cmd == CC_BALISE_ENODE): # CS enodeString
			print("0x01 OK : enodeString transfert")
			size = int.from_bytes(connexion.recv(CC_LEN_OF_SIZE), byteorder='big')
			print("size of enode in byte : " + str(size))
			 

	
	
	



def start_server(w3):
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
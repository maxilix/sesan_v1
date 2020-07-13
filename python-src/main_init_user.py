
import	subprocess
import	re

DEFAULT_NODE_NAME			= "foo"
DEFAULT_CONSENSUS 			= "clique"
DEFAULT_CONNEXION_TYPE		= "server"
DEFAULT_USER_TYPE 			= "asso"


print("Init ethereum Sesan Blockchain with geth")




print("Check geth installation")
proc = subprocess.Popen('''geth version''', shell=True, stdout=subprocess.PIPE)
outs, errs = proc.communicate(timeout=15)
if (outs[:4].decode('UTF-8') != "Geth"):
	raise NameError("Geth seems uninstalled")

nodeName = "."
while (bool(re.compile(r'[^a-z]').search(nodeName))):
	nodeName = input("Node name (ascii lowercase lettre only)(a-z) : ") or DEFAULT_NODE_NAME
print("Node name : " + nodeName)

consensus = "."
while (consensus != "clique" and consensus != "ethash"):
	consensus = input("Consensus type (clique or ethash) : ") or DEFAULT_CONSENSUS
print("Consensus : " + consensus)

connexionType = "."
while (connexionType != "client" and connexionType != "server"):
	connexionType = input("Connexion type (client or server) : ") or DEFAULT_CONNEXION_TYPE
print("Connexion type : " + connexionType)

userType = "."
while (userType != "user" and userType != "asso" and userType != "pro" and userType != "health"):
	userType = input("User type (user, asso, pro or health) : ") or DEFAULT_USER_TYPE
print("User type : " + userType)


#if (connexionType == "server" and (userType == "asso" or userType == "pro" or userType == "health")



proc = subprocess.Popen('''geth --datadir ./eth-{0} init {1}_genesis.json'''.format(nodeName,consensus), shell=True, stdout=subprocess.PIPE)

outs, errs = proc.communicate(timeout=60)

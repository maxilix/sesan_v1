
import subprocess



print("Init ethereum Sesan Blockchain with geth")

"""
proc = subprocess.Popen('''geth version''', shell=True, stdout=subprocess.PIPE)
try:
	outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
	proc.kill()
	outs, errs = proc.communicate()

if (outs[:4].decode('UTF-8') != "Geth")

# if ! type geth 2> /dev/null; then echo "not"; fi
"""

nodeName = None
while (nodeName == None):
	nodeName = input("Node name (ascii lowercase lettre only) : ")
	# TODO check valid name

consensus = None
while (consensus != "clique" and consensus != "ethash"):
	consensus = input("Consensus type (clique or ethash) : ")

proc = subprocess.Popen('''geth --datadir ./eth-{0} init {1}_genesis.json'''.format(nodeName,consensus), shell=True, stdout=subprocess.PIPE)
try:
	outs, errs = proc.communicate(timeout=60)
except TimeoutExpired:
	proc.kill()
	print("communication error with geth init.")

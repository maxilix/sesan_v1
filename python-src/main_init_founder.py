import	subprocess
import	re


GENESIS_FILE_NAME			= "sesan_clique_genesis.json"

DEFAULT_FOUNDER_NODENAME	= "marie"
DEFAULT_FOUNDER_PASSWORD	= DEFAULT_FOUNDER_NODENAME
DEFAULT_CHAIN_ID			= 1222
DEFAULT_CHAIN_PERIOD		= 10


"""
	echo -n "marie" | openssl sha256 -binary -out marie_password.key
	geth --datadir ./eth_marie/ --password marie_password.key account new
		recup 0xa3f0ac4e5b5aa6a4c72d1fb7cef4936a2cc4a357
	geth --datadir eth_marie/ init test_clique_genesis.json
"""


def create_genesis_file(founderAddress): # founderAddress on 40 char without "0x"
	genesis 							= dict()
	genesis["config"]						= dict()
	genesis["config"]["chainId"]				= int(input("chainId : ") or DEFAULT_CHAIN_ID )
	genesis["config"]["homesteadBlock"]			= 0
	genesis["config"]["eip150Block"]			= 0
	genesis["config"]["eip150Hash"]				= "0x0000000000000000000000000000000000000000000000000000000000000000"
	genesis["config"]["eip155Block"]			= 0
	genesis["config"]["eip158Block"]			= 0
	genesis["config"]["byzantiumBlock"]			= 0
	genesis["config"]["constantinopleBlock"]	= 0
	genesis["config"]["petersburgBlock"]		= 0
	genesis["config"]["istanbulBlock"]			= 0
	genesis["config"]["clique"]					= dict()
	genesis["config"]["clique"]["period"]			= int(input("block period (in second) : ") or DEFAULT_CHAIN_PERIOD )
	genesis["config"]["clique"]["epoch"]			= 30000
	genesis["nonce"]							= "0x0"
	genesis["timestamp"]						= "0x00000000"
	genesis["extraData"]						= "0x0000000000000000000000000000000000000000000000000000000000000000" + founderAddress + "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
	genesis["gasLimit"]							= "0xffffff"
	genesis["difficulty"]						= "0x1"
	genesis["mixHash"]							= "0x0000000000000000000000000000000000000000000000000000000000000000"
	genesis["coinbase"]							= "0x" + founderAddress
	genesis["alloc"]							= dict()
	genesis["alloc"][founderAddress]					= dict()
	genesis["alloc"][founderAddress]["balance"]			= "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
	genesis["number"]							= "0x0"
	genesis["gasUsed"]							= "0x0"
	genesis["parentHash"]						= "0x0000000000000000000000000000000000000000000000000000000000000000"

	genesisFile = open(GENESIS_FILE_NAME, "w")
	genesisFile.write(str(genesis).replace("'",'"'))
	genesisFile.write("\n")
	genesisFile.close()





# founder node name
nodeName = "."
while (bool(re.compile(r'[^a-z]').search(nodeName))):
	nodeName = input("Founder node name (ascii lowercase lettre only)(a-z) : ") or DEFAULT_FOUNDER_NODENAME

# create founder directory
founderDirectory = "./eth_{0}/".format(nodeName)
subprocess.run("mkdir {0}".format(founderDirectory), shell=True, stdout=subprocess.PIPE)


# create founder password file
founderPasswordFile = open(founderDirectory + nodeName + "_password.key","w")
founderPasswordFile.write(input(nodeName + "'s password : ") or DEFAULT_FOUNDER_PASSWORD)
founderPasswordFile.close()


# create founder account
proc = subprocess.Popen("geth --datadir {0} --password {0}{1}_password.key account new".format(founderDirectory, nodeName), shell=True, stdout=subprocess.PIPE)
out,err = proc.communicate()
founderAddress = out.decode('UTF-8')[60:100].lower()


# create genesis file
create_genesis_file(founderAddress)


# init geth node
subprocess.run("geth --datadir {0} init {1}".format(founderDirectory,GENESIS_FILE_NAME), shell=True, stdout=subprocess.PIPE)


print("\n\n" + nodeName + "'s node initialized.\nPy server can be launched.\n")
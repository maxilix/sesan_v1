


#################################   DEBUG   ####################
DEFAULT_NODE_NAME						= "marie"
CONTRACT_STORAGE_SOURCES_FILENAME		= "strorage.sol"

################################################################



#################################   SYSTEM   ###################
DEFAULT_VERBOSITY			= 3
#							0 no Log
#							1 only Error
# 							2 Warn and Error
# 							3 Warn, Error and Info
# 							4 Warn, Error, Info and NoFlag
# 							5 Warn, Error, Info, NoFlag and CC (without PING/PONG)
#							6 All
CONFIG_FILENAME				= ".conf.json"

################################################################



#################################   LOG   ######################
LOG_SERVER_FILENAME			= ".server.log"
LOG_GETH_FILENAME			= ".geth.log"

LOG_FLAG_SECURE_EXIT		= 0
LOG_FLAG_ERROR				= 1
LOG_FLAG_WARN				= 2
LOG_FLAG_INFO				= 3
LOG_FLAG_NOFLAG				= 4
LOG_FLAG_CC					= 5

LOG 						= "log"
STDOUT 						= "stdout"
STDERR						= "stderr"
################################################################



#################################   GETH   #####################

GETH_MAX_PEER_ENODE_SENT			= 20
GETH_PERCENT_PEER_ENODE_SENT		= 10

GETH_MAX_MINING_THREAD 				= 2
################################################################

#################################   CONTRACT   #################
CONTRACT_SOURCES_FOLDER					= "./sol_src/"
CONTRACT_EIGENTRUST_SOURCES_FILENAME	= "eigenTrust.sol"
CONTRACT_IM_SOURCES_FILENAME			= "interventionManager.sol"
CONTRACT_PORX_SOURCES_FILENAME			= "PoRX.sol"
################################################################



#################################   SERVER   ###################

################################################################



#################################   CLIENT_COMMUNICATION   #####
CC_TIMEOUT 							= 10
CC_LEN_OF_SIZE 						= 2


# 0 system
CC__START							= b'\x00'
CC__STOP							= b'\x00'
CC__PING							= b'\x01'
CC__PONG							= b'\x02'

# 1 recieve
CC__RECIEVE_ENODE					= b'\x10'
CC__RECIEVE_ADDRESS					= b'\x11'

# 2 user request
CC__REQUEST_SERVER_ENODE			= b'\x20'
CC__REQUEST_PEERS_ENODE				= b'\x21'
CC__REQUEST_SERVER_ADDRESS			= b'\x22'
CC__REQUEST_PEERS_ADDRESS			= b'\x23'
CC__REQUEST_CONTRACT_IM				= b'\x24'
CC__REQUEST_CONTRACT_EIGENTRUST		= b'\x25'
CC__REQUEST_NETWORKID				= b'\x26'
CC__REQUEST_ETHER					= b'\x27'

# 3 authentification
CC__SERVER_COMMITMENT				= b'\x30'
CC__SERVER_ASSO_LOGIN				= b'\x31'
CC__SERVER_PRO_LOGIN				= b'\x32'
CC__SERVER_HEALT_LOGIN				= b'\x33'

# 4 authorized request
CC__REQUEST_PREFOUND_ADDRESS		= b'\x40'
CC__REQUEST_PREFOUND_PASSWORD		= b'\x41'
CC__REQUEST_ETHER_PART				= b'\x42'

# 5 clique engine
CC__REQUEST_PROPOSE					= b'\x50'
CC__REQUEST_DISPOSE					= b'\x51'

# 6 acknowledgment
CC__REQUEST_PROPOSE_AKW				= b'\x60'
CC__REQUEST_DISPOSE_AKW				= b'\x61'
CC__REQUEST_ETHER_AKW				= b'\x62'
################################################################



#################################   CLIENT UPDATE   ############
# MS bit : socket usable
# 2e bit : need update
# 3e bit : 
# 4e bit : 
# 5e bit : 
# 6e bit : 
# 7e bit : 
# LS bit : 

C_NO_UPDATE 						= 0b00000000
C_UPDATE_ADDRESS					= 0b00000001
C_UPDATE_PEERABLE					= 0b00000010


################################################################

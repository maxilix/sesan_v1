


#################################   DEBUG   ####################
DEBUG_DEFAULT_NODENAME		= "aspr"
################################################################



#################################   LOG   ######################
LOG_PATHFILE				= "./log"

LOG_FLAG_NOFLAG				= 0
LOG_FLAG_INFO				= 1
LOG_FLAG_WARNING			= 2
LOG_FLAG_ERROR				= 3
################################################################



#################################   GETH   #####################
GETH_NETWORKID				= 1789
GETH_SUBPROCESS_COMMAND		= ""								# TODO
################################################################



#################################   GETH   #####################
SERVER_LISTEN_PORT			= 30302
################################################################



#################################   CLIENT_COMMUNICATION   #####
CC_TIMEOUT 					= 10
CC_LEN_OF_SIZE 				= 1


# 0 system
CC__START							= b'\x00'
CC__STOP							= b'\x00'
CC__PING							= b'\x01'
CC__PONG							= b'\x02'

# 1 sending
CC__SEND_ENODE						= b'\x10'
CC__SEND_ADDRESS					= b'\x11'

# 2 user request
CC__REQUEST_ENODE_SERVER			= b'\x20'
CC__REQUEST_ENODE_PEERS				= b'\x21'
CC__REQUEST_ADDRESS_SERVER			= b'\x22'
CC__REQUEST_ADDRESS_PEERS			= b'\x23'
CC__REQUEST_CONTRACT_GI				= b'\x24'
CC__REQUEST_CONTRACT_EIGENTRUST		= b'\x25'
CC__REQUEST_NETWORKID				= b'\x26'

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

################################################################



#################################   CMD INTERPRETOR   ##########
CMD__EXIT							= "exit"
CMD__CLIENT_LIST					= "clients"
CMD__CLIENT_I 						= "client"
CMD__CLOSE_CLIENT_CONNEXION			= "close_client"
CMD__CLOSE_SERVER_CONNEXION			= "close_server"

################################################################

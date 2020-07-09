




#################################   DEBUG   ####################
DEBUG_DEFAULT_NODENAME		= "kevin"
################################################################



#################################   LOG   ######################
LOG_PATHFILE				= "./log"

LOG_FLAG_INFO				= 1
LOG_FLAG_WARNING			= 2
LOG_FLAG_ERROR				= 4
################################################################



#################################   GETH   #####################
GETH_NETWORKID				= 1789
GETH_SUBPROCESS_COMMAND		= ""								# TODO
################################################################



#################################   CLIENT_COMMUNICATION   #####
CC_TIMEOUT 					= 10
CC_LEN_OF_SIZE 				= 1


# 0 system
CC_BALISE_START				= b'\x00'
CC_BALISE_STOP				= b'\x00'
CC_BALISE_PING				= b'\x01'
CC_BALISE_PONG				= b'\x02'

# 1 sending
CC_BALISE_SEND_ENODE		= b'\x10'

# 2 request
CC_BALISE_REQUEST_ENODE		= b'\x20'
################################################################

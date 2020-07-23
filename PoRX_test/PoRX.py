import hashlib
import random
import threading
import time
import sys





GENESIS_HEADER 			= 0
GENESIS_NONCE 			= 0
GENESIS_BLOCK 			= { "header" : GENESIS_HEADER,
                            "nonce"  : GENESIS_NONCE,
                            "miner"  : "no miner" }

DIFFICULTY_THRESHOLD 	= 0x0080000000000000000000000000000000000000000000000000000000000000


REPUTATION_INIT 		= 1000
REPUTATION_MIN 			= 0
REPUTATION_MAX 			= 2000
REPUTATION_RATIO 		= 1
EXP_BASE 				= 1.7

reputation 				= {}

MINER_NUMBER 			= 3
BLOCK_NUMBER_TEST		= 5000


C_DURATION				= MINER_NUMBER * 2 #6
C_REWARD 				= C_DURATION * 2 #8
C_DECAY 				= C_DURATION * 3 #10

S_REWARD 				= int(C_DURATION * 2/3) #4
S_DECAY 				= int(C_DURATION * 1/5) #1

D_REWARD 				= 100
D_DECAY 				= 30


blocks = []
blocks.append(GENESIS_BLOCK)





# header est un uint256
# nonce  est un uint256
# hash retourne un uint256
def hash(header,nonce):
	return int(hashlib.sha256(("{0:064x}{1:064x}".format(header,nonce)).encode()).hexdigest(),16)

def block_number():
	return len(blocks)

def count_of(miner):
	count = 0
	for b in blocks:
		if (b["miner"] == "miner-{0:02}".format(miner)):
			count += 1
	return count

def print_stats():
	print("blocks : " + str(BLOCK_NUMBER_TEST))
	print("miners : " + str(MINER_NUMBER))
	for i in range(MINER_NUMBER):
		count = count_of(i)
		print("\tminer-{0:02}\t\t{1:5}\t\t{2:2.2f}".format(i+1,count,count/BLOCK_NUMBER_TEST*100))

def write_reputation_file(fd):
	fd.write("{0:5}".format(len(blocks)))
	for i in range(MINER_NUMBER):
		fd.write("   {0:4}".format(reputation["miner-{:02}".format(i)]))
	fd.write("\n")
	fd.flush()







def count_on(duration):
	count = 0
	for i in range(duration):
		tested = len(blocks)-i-1
		if (tested < 0):
			break
		if (blocks[tested]["miner"] == threading.currentThread().name):
			count += 1
	return count



def difficulty_threshold():
	difficulty = int(2**256/DIFFICULTY_THRESHOLD)
	personalDifficulty = int(difficulty + ((REPUTATION_INIT - usable_reputation())*difficulty*REPUTATION_RATIO)/REPUTATION_INIT)
	if (personalDifficulty == 0):
		return 2**256
	else:
		return int(2**256/personalDifficulty)

def usable_reputation():
	count = count_on(C_DURATION)
	return int(reputation[threading.currentThread().name] / EXP_BASE**count)



def update_reward_reputation():
	currentReputation = reputation[threading.currentThread().name]
	countReward = count_on(C_REWARD)
	eReward = min(1, (countReward*C_DURATION*REPUTATION_MAX)/(C_REWARD * currentReputation * S_REWARD))
	reputation[threading.currentThread().name] = int(currentReputation + (1-eReward)*(REPUTATION_MAX-currentReputation)/D_REWARD)

def update_decay_reputation():
	currentReputation = reputation[threading.currentThread().name]
	countDecay = count_on(C_DECAY)
	eDecay = min(1, (countDecay*C_DURATION*REPUTATION_MAX)/(C_DECAY * currentReputation * S_DECAY))
	reputation[threading.currentThread().name] = int(currentReputation - (1-eDecay)*currentReputation/D_DECAY)

def run_cpu():
	while (len(blocks) < BLOCK_NUMBER_TEST):
		currentBlock = blocks[-1]
		d = difficulty_threshold()
		nonce = int(random.uniform(0, 2**256-1))
		while (currentBlock == blocks[-1]):
			h = hash(currentBlock["header"], nonce)
			if (h <= d):
				blocks.append({ "header" : h,
                                "nonce"  : nonce,
                                "miner"  : threading.currentThread().name })
				update_reward_reputation()
				break
			else:
				nonce += 1
				if (nonce == 2**256):
					nonce = 0

		if (len(blocks) % C_DECAY == 0):
			update_decay_reputation()



def start_node(reputationInit,power):
	reputation[threading.currentThread().name] = reputationInit
	unit = [None]*power
	for i in range(power):
		unit[i] = threading.Thread(target=run_cpu, name=threading.currentThread().name, args=( ), daemon=True)
	for u in unit:
		u.start()







power = [1]*MINER_NUMBER
power[0] = 3
power[1] = 1
power[2] = 1

initialReputation = [REPUTATION_INIT]*MINER_NUMBER
#r[0] =  500
#r[1] = 1000
#r[2] = 1500


thread = [None]*MINER_NUMBER
for i in range(MINER_NUMBER):
	thread[i] = threading.Thread(target=start_node, name="miner-{:02}".format(i), args=(initialReputation[i], power[i], ), daemon=True)


#fr = [None]*MINER_NUMBER
#for i in range(MINER_NUMBER):
#	fr[i] = open("r{:02}.txt".format(i), 'w')

reputationFile = open("r.txt",'w')


for t in thread:
	t.start()


# join
while (len(blocks) < BLOCK_NUMBER_TEST):
	sys.stdout.write("\r{:2.2f}%".format(len(blocks)/BLOCK_NUMBER_TEST*100))
	sys.stdout.flush()

	#fr[int(threading.currentThread().name[-2:])].write(str(reputation[threading.currentThread().name])+"\n")
	#fr[int(threading.currentThread().name[-2:])].flush()
	write_reputation_file(reputationFile)
	currentBlock = blocks[-1]
	while (currentBlock == blocks[-1] and len(blocks) < BLOCK_NUMBER_TEST):
		time.sleep(0.1)


#for file in fr:
#	file.close()
reputationFile.close()


print("\n")

print_stats()



"""
newNode = threading.Thread(target=start_node, name="miner-{0:02}".format(n), args=( ), deamon True)
newNode.start()


while len(blocks)<10:

	nonce = 0
	blockNumber = len(blocks)
	while True:
		h = hash(blocks[blockNumber-1][0],nonce)
		if (h <= difficulty):
			blocks.append([h,nonce])
			print("block {0} : {1:064x}".format(blockNumber,h))
			break
		else:
			nonce += 1
"""




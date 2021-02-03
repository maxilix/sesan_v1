import 	time
import	threading



from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console



def start_spy():
	console(LOG_FLAG_INFO, "start PoRX spy" , who="PoRX")
	events = dict()
	events["SubmitNonce"] = tools.PoRX.events.SubmitNonce.createFilter(fromBlock=0)
	events["MinerAdded"] = tools.PoRX.events.MinerAdded.createFilter(fromBlock=0)
	events["MinerRevoked"] = tools.PoRX.events.MinerRevoked.createFilter(fromBlock=0)

	while (threading.currentThread().name == "PoRXSpyThread"):
		check_events(events)
		time.sleep(1)


	console(LOG_FLAG_INFO, "PoRX spy stopped" , who="PoRX")


def check_events(events):
	# SubmitNonce event
	news = events["SubmitNonce"].get_new_entries()
	for e in news:
		if (e["args"]["valid"]):
			console(LOG_FLAG_INFO, "{0} found {1} for the block {2}".format(e["args"]["miner"],e["args"]["nonce"],e['blockNumber']) , who="PoRX")
		else:
			console(LOG_FLAG_INFO, "{0} failed with {1}".format(e["args"]["miner"],e["args"]["nonce"]) , who="PoRX")

	# MinerAdded event
	news = events["MinerAdded"].get_new_entries()
	for e in news:
		console(LOG_FLAG_INFO, "{0} added {1} at block {2}".format(e["args"]["authority"],e["args"]["miner"],e['blockNumber']) , who="PoRX")

	# MinerRevoked event
	news = events["MinerRevoked"].get_new_entries()
	for e in news:
		console(LOG_FLAG_INFO, "{0} revoked {1} at block {2}".format(e["args"]["authority"],e["args"]["miner"],e['blockNumber']) , who="PoRX")

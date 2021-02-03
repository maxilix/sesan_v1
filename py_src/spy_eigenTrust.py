import 	time
import	threading
import 	math



from	settings		import	*

import	server_tools	as 		tools
from	server_tools	import	console



def start_spy():
	console(LOG_FLAG_INFO, "start eigenTrust spy" , who="eigenTrust")
	events = dict()
	events["NewUser"] = tools.eigenTrust.events.NewUser.createFilter(fromBlock=0)
	events["Vote"] = tools.eigenTrust.events.Vote.createFilter(fromBlock=0)

	while (threading.currentThread().name == "eigenTrustSpyThread"):
		check_events(events)
		time.sleep(1)


	console(LOG_FLAG_INFO, "eigenTrust spy stopped" , who="eigenTrust")


def check_events(events):
	# NewUser event
	news = events["NewUser"].get_new_entries()
	for e in news:
		console(LOG_FLAG_INFO, "{0} : {1} added".format(e["args"]["index"],e["args"]["user"]) , who="eigenTrust")

	# Vote event
	news = events["Vote"].get_new_entries()
	for e in news:
		if (e["args"]["vote"]):
			console(LOG_FLAG_INFO, "{0} vote for {1}".format(e["args"]["from"],e["args"]["to"]) , who="eigenTrust")
		else:
			console(LOG_FLAG_INFO, "{0} vote against {1}".format(e["args"]["from"],e["args"]["to"]) , who="eigenTrust")


def get_normalize_local_trust_matrix():
	s = tools.eigenTrust.functions.get_s().call()
	users = tools.eigenTrust.functions.get_users().call()
	p = get_preTrusted_vector()

	c = [[0]*len(users) for i in range(len(users))]
	for i in range(len(users)):
		tempSum = 0
		for j in range(len(users)):
			tempSum += max(s[i][j],0)
		if (tempSum == 0):
			for j in range(len(users)):
				c[i][j] = p[i]
		else:
			for j in range(len(users)):
				c[i][j] = max(s[i][j],0)/tempSum
	return c

def get_preTrusted_vector():
	p = tools.eigenTrust.functions.get_p().call()
	pTrustValue = 1/p.count(True)
	return [pTrustValue if preTrusted else 0 for preTrusted in p]

def euclidean_distance(a,b):
	if (len(a)!=len(b)):
		raise NameError("eigenTrust : euclidean_distance() : a and b must be same length")

	s = 0
	for i in range(len(a)):
		s += (a[i]-b[i])**2
	return math.sqrt(s)


def get_normalize_global_trust_matrix(epsilon = 0.1, alpha = None):
	if (alpha == None):
		alpha = tools.eigenTrust.functions.get_alpha().call()/2**256

	if (alpha < 0 or alpha > 1):
		raise NameError("eigenTrust : get_normalize_global_trust_matrix : alpha must be in [0;1]")

	p = get_preTrusted_vector()
	c = get_normalize_local_trust_matrix()
	n = len(p)
	if (n != len(c)):
		raise NameError("eigenTrust : get_normalize_global_trust_matrix : wrong init of n")

	temp = [0]*n
	t = p.copy()
	while (euclidean_distance(temp,t) >= epsilon):
		for i in range(n):
			tempSum = 0
			for j in range(n):
				tempSum += c[j][i] * t[j]
			temp[i] = (1 - alpha) * tempSum  +  alpha * p[i]
		t = temp.copy()

	return t







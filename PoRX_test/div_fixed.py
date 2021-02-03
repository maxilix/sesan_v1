op1 = 1.5
op2 = 2


"""
def div(op1I,op1D,op2):
	if (op2 == 0):
		print("division by zero")
		return 0,0
	elif (op2 == 1):
		return op1I,op1D
	else:
		rI = op1I//op2
		rest = op1I-rI*op2
		rD = (2**256*rest + op1D) // op2
		return rI,rD
"""
def div(op1I,op1D,op2I,op2D):
	q = 0
	while


def eval(ufp):
	return ufp[0] + ufp[2]/2**256


r = div(1,0.5*2**256,2)
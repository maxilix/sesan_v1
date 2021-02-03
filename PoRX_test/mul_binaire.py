

a = [ True , False, False,  True , True , False, False, False ] # 
b = [ True , False, False,  True , True , False, False, False ] # 


def maj(a,b,c):
	return b&c|a&c|a&b|a&b&c


r = [False]*16
for j in range(8):
	if (b[j] == True):
		c = False
		for i in range(8):
			m = maj(r[i+j],a[i],c)
			r[i+j] = r[i+j] ^ a[i] ^ c
			if (m == True):
				c = True
			else:
				c = False
		r[j+8] = c




print(r)



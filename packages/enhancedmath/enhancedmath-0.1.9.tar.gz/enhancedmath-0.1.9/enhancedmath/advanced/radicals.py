import math

def sqrt(x):
	if type(x) == int:
		return math.sqrt(x)
	if type(x) == float:
		y = round(x)
		return y

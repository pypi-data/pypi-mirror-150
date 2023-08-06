import math

def sqrt(x):
	if type(x) == int:
		print(math.sqrt(x))
	if type(x) == float:
		y = math.sqrt(x)
		z = round(y)
		print(z)
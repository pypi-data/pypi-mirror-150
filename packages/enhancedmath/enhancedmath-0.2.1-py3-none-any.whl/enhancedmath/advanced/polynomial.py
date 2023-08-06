def findMonomialDegree(x):
  for character in str(x):
    if character.isdigit(0):
      print("Constant")
    if character.isdigit(1):
      print("Linear")
    if character.isdigit(2):
      print("Quadratic")
    if character.isdigit(3):
      print("Cubic")
    if character.isdigit(4):
      print("4th Degree")
    if character.isdigit(5):
      print("5th Degree")
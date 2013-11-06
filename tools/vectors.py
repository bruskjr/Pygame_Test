import math

class Vector2:

	def __init__(self, x, y=None):
		if y == None:
			self.x = x[0]
			self.y = x[1]
		else:
			self.x = x
			self.y = y

	def __len__(self):
		return 2

	def __getitem__(self, key):
   		if key == 0:
			return self.x
		elif key == 1:
			return self.y

	def __setitem__(self, key, value):
		if key== 0:
			self.x = value
		elif key == 1:
			self.y = value

	def __repr__(self):
		return "(%s,%s)" % (self.x,self.y)

	def __add__(self, other):
		return Vector2(self.x+other.x, self.y+other.y)
	__radd__ = __add__


	def __sub__(self, other):
		return Vector2(self.x-other.x, self.y-other.y)

	def __div__(self,other):
		return Vector2(self.x/float(other.x), self.y/float(other.y))

	def length(self):
  		return math.sqrt(self.x**2 + self.y**2)
    
	def normalize(self):
		return self/Vector2(self.length(), self.length())

	def angle(self):
		return math.degrees(math.atan2(self.y, self.x))
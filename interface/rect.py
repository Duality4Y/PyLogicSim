import collections

class Rect(object):
	def __init__(self, *args):
		print(f"args: {args}")
		print(f"args[0]: {args[0]}")
		if isinstance(args, collections.Sequence):
			if isinstance(args[0], collections.Sequence):
				self.rectValues = list(args[0])
			else:
				self.rectValues = args
		# if isinstance(args, collections.Sequence):
		# 	print(f"Sequence: {args}")
		# 	self.rectValues = args[0]
		# else:
		# 	print(f"Non sequence: {args}")
		# 	self.rectValues = args
		print(f"self.rectValues = {self.rectValues}")

	@property
	def x(self):
		return self.rectValues[0]
	@x.setter
	def x(self, x):
		_, y, width, height = self.rectValues
		self.rectValues = x, y, width, height

	@property
	def y(self):
		return self.rectValues[1]
	@y.setter
	def y(self, y):
		x, _, width, height = self.rectValues
		self.rectValues = x, y, width, height

	@property
	def width(self):
		return self.rectValues[2]
	@width.setter
	def width(self, width):
		x, y, _, height = self.rectValues
		self.rectValues = x, y, width, height

	@property
	def height(self):
		return self.rectValues[3]
	@height.setter
	def height(self, height):
		x, y, width, _ = self.rectValues
		self.rectValues = x, y, width, height

	def __getitem__(self, key):
		return self.rectValues.__getitem__(key)

	def __setitem__(self, key, value):
		self.rectValues.__setitem__(key, value)

	def __repr__(self):
		return self.rectValues.__repr__()
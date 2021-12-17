class Rect(object):
	def __init__(self, *args):
		self.rectValues = list(args)

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
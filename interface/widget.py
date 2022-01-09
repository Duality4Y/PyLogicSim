import pygame

DebugDraw = True

""" Basic Widget object that determines what other elements should look like"""
class Widget(object):
	(EXPAND,
	 FILL,
	 FIXED) = [i for i in range(0, 3)]
	def __init__(self, *args, **kwargs):
		self.offset = (0, 0)
		self.area = None
		self.rect = kwargs.get("rect", (0, 0, 100, 100))

		self.parent = None

		self.id = kwargs.get("id")

		self.behaviour = Widget.EXPAND

		self.borderColor = (0, 0, 0xff)
		self.crossColor1 = (0xff, 0, 0)
		self.crossColor2 = (0, 0xff, 0)
	
	def debugPrintParents(self):
		print(f"child({type(self).__name__})->parent->", end="")
		parent = self.parent
		while parent:
			print(f"{type(parent).__name__}", end="")
			parent = parent.parent
			if parent:
				print("->", end="")
		print()

	def setParent(self, parent):
		self.parent = parent
	
	def assignArea(self, area):
		# print(f"widget({self})->area: {area}")
		self.area = area

	def update(self):
		if self.behaviour == Widget.EXPAND:
			self.rect = self.area
		elif self.behaviour == Widget.FILL:
			self.rect = self.area
		elif self.behaviour == Widget.FIXED:
			return;

	""" This functions allows for the drawing of a border """
	def drawBorder(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.rect, 1)
	""" This function draws the widget """
	def draw(self, surface):
		if DebugDraw == False:
			return
		""" draw a basic border to indicate widget location and size """
		self.drawBorder(surface)
		""" a cross to make clear where the corners are and where the middle is in relation to other things. """
		x, y, width, height = self.rect
		pygame.draw.line(surface, self.crossColor1, (x, y), (x + width, y + height), 1)
		pygame.draw.line(surface, self.crossColor2, (x, y + height), (x + width, y), 1)
	""" this function sets the internal state based on outside events."""
	def handleEvents(self, event):
		pass
	""" process previously set state to generate events and call calbacks if needed."""
	def processEvents(self):
		pass
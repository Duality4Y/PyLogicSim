import pygame

DebugDraw = True

""" Basic Widget object that determines what other elements should look like"""
class Widget(object):
	def __init__(self, *args, **kwargs):
		self.offset = (0, 0)
		self.rect = kwargs.get("rect", (0, 0, 100, 100))

		self.parent = None

		self.id = kwargs.get("id")

		self.borderColor = (0, 0, 0xff)
		self.crossColor1 = (0xff, 0, 0)
		self.crossColor2 = (0, 0xff, 0)

	def setParent(self, parent):
		self.parent = parent

	def setOffset(self, offset):
		self.offset = offset

	def applyOffset(self, rect):
		xo, yo = self.offset
		x, y, width, height = rect
		return (x + xo, y + yo, width, height)

	def update(self):
		pass

	""" This functions allows for the drawing of a border """
	def drawBorder(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.applyOffset(self.rect), 1)
	""" This function draws the widget """
	def draw(self, surface):
		if DebugDraw == False:
			return
		""" draw a basic border to indicate widget location and size """
		self.drawBorder(surface)
		""" a cross to make clear where the corners are and where the middle is in relation to other things. """
		x, y, width, height = self.applyOffset(self.rect)
		pygame.draw.line(surface, self.crossColor1, (x, y), (x + width, y + height), 1)
		pygame.draw.line(surface, self.crossColor2, (x, y + height), (x + width, y), 1)
	""" this function sets the internal state based on outside events."""
	def handleEvents(self, event):
		pass
	""" process previously set state to generate events and call calbacks if needed."""
	def processEvents(self):
		pass
import pygame

from interface.rectUtils import *
from interface.colorDefs import *

DebugDraw = True
DebugDraw = False

""" Basic Widget object that determines what other elements should look like"""
class Widget(object):
	(EXPAND,
	 FILL,
	 FIXED) = [i for i in range(0, 3)]
	def __init__(self, *args, **kwargs):
		self.id = kwargs.get("id", None)

		self.parent = None

		self.area = kwargs.get("area", (0, 0, 100, 100))
		
		self.contentArea = (0, 0, 100, 100)
		self.paddingArea = (0, 0, 100, 100)
		self.borderArea = (0, 0, 100, 100)
		self.marginArea = (0, 0, 100, 100)

		self.marginSize = 3
		self.borderSize = 1
		self.paddingSize = 2

		self.borderColor = (0x80, 0x80, 0x80)
		self.borderBgColor = (0x00, 0x00, 0x00)
		self.borderFill = 2
		self.cornerRatio = 24
		self.borderVisible = True

		self.visible = True

		self.bgColor = (0x10, 0x28, 0x50)

		self.behaviour = kwargs.get("behaviour", Widget.EXPAND)

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

	def setPosition(self, pos):
		self.area = setAreaPosition(pos, self.area)
	
	def getPosition(self):
		area = getAreaPosition(self.area)
		return area

	def setParent(self, parent):
		self.parent = parent
	
	def assignArea(self, area):
		# if self.behaviour is not Widget.FIXED:
		# 	oriX, oriY = getAreaPosition(self.area)
		# 	x, y, width, height = area
		# 	self.area = oriX + x, oriY + y, width, height
		xo, yo = 0, 0
		if self.behaviour is Widget.FIXED:
			xo, yo = getAreaPosition(self.area)

		x, y, width, height = area
		self.area = xo + x, yo + y, width, height
	
	def calculateAreaRect(self):
		pos = self.getPosition()
		_, _, contentWidth, contentHeight = self.contentArea
		areaWidth, areaHeight = self.paddingSize * 2 + \
								self.marginSize * 2 + \
								self.borderSize *2  + \
								contentWidth, \
								self.paddingSize * 2 + \
								self.marginSize * 2 + \
								self.borderSize * 2 + \
								contentHeight
		return *pos, areaWidth, areaHeight

	def update(self):
		if self.behaviour == Widget.EXPAND:
			self.marginArea = self.area
			self.borderArea = shrinkArea(self.marginArea, size=self.marginSize)
			self.paddingArea = shrinkArea(self.borderArea, size=self.borderSize)
			self.contentArea = shrinkArea(self.paddingArea, size=self.paddingSize)
		elif self.behaviour == Widget.FILL:
			self.marginArea = self.area
			self.borderArea = self.marginArea
			self.paddingArea = shrinkArea(self.borderArea, size=self.borderSize)
			self.contentArea = shrinkArea(self.paddingArea, size=self.paddingSize)
		elif self.behaviour == Widget.FIXED:
			self.area = self.calculateAreaRect()
			self.marginArea = self.area
			self.borderArea = shrinkArea(self.marginArea, size=self.marginSize)
			self.paddingArea = shrinkArea(self.borderArea, size=self.borderSize)
			self.contentArea = shrinkArea(self.paddingArea, size=self.paddingSize)

		
	""" a cross to make clear where the corners are and where the middle is in relation to other things. """
	def drawCross(self, surface):
		x, y, width, height = self.rect
		pygame.draw.line(surface, self.crossColor1, (x, y), (x + width, y + height), 1)
		pygame.draw.line(surface, self.crossColor2, (x, y + height), (x + width, y), 1)
	
	# def colorSurface(self, area, color, alpha=80):
	# 	surface = pygame.Surface(getAreaSize(area))
	# 	surface.fill(color)
	# 	surface.set_alpha(alpha)
	# 	return surface, getAreaPosition(area)
	""" Draws a debug layout in contrasting colors."""
	def drawLayout(self, surface):
		pygame.draw.rect(surface, GREEN, self.marginArea, 0)
		pygame.draw.rect(surface, MAGENTA, self.borderArea, 0)
		pygame.draw.rect(surface, CYAN, self.paddingArea, 0)
		pygame.draw.rect(surface, YELLOW, self.contentArea, 0)

	""" This function allows for drawing a background. """
	def drawBackground(self, surface):
		bgSurface = pygame.Surface(getAreaSize(self.contentArea))
		bgSurface.fill(self.bgColor)
		bgSurface.set_alpha(0x80)
		pygame.draw.rect(surface, (0, 0, 0), self.area, 0)
		# pygame.draw.rect(surface, self.bgColor, self.contentArea, 0)
		surface.blit(bgSurface, getAreaPosition(self.contentArea))

	""" This function allows for drawing of the border """
	def drawBorder(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.borderArea, self.borderSize)

	""" This function allows for drawing the content of the widget. """
	def drawContent(self, surface):
		pass
	
	""" This function draws the widget """
	def draw(self, surface):
		if not self.visible:
			return
		""" Draw the background first. """
		self.drawBackground(surface)
		""" if enabled draws the layout for debugging purposes. """
		if DebugDraw:
			self.drawLayout(surface)
		""" draw the widget contents"""
		self.drawContent(surface)
		""" draw a basic border to indicate widget location and size """
		if self.borderVisible:
			self.drawBorder(surface)
	
	""" this function sets the internal state based on outside events."""
	def handleEvents(self, event):
		pass
	
	""" process previously set state to generate events and call calbacks if needed."""
	def processEvents(self):
		pass
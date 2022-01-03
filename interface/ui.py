import pygame
import pygame.freetype
import time

import os
import sys

pygame.init()
pygame.font.init()

moduleFilePath = os.path.abspath(sys.modules['__main__'].__file__)
projectRoot = os.path.dirname(moduleFilePath)

screenSize = screenWidth, screenHeight = 800, 600
screen = pygame.display.set_mode(screenSize)

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

Running = True

fontName = "Roboto-Regular.ttf"
fontSize = 18

fontResourcePath = os.path.join(projectRoot, "resources/fonts")
fontPath = os.path.join(fontResourcePath, fontName)
print(f"{__name__} : loading font: {fontPath}")
UIFont = pygame.freetype.Font(fontPath, fontSize)


DebugDraw = True

class Alignment(object):
	(CENTER,
	 LEFT,
	 RIGHT) = [i for i in range(0, 3)]
	def __init__(self):
		pass
	"""
		calculate rect2 alignment relative to rect1 with padding
	"""
	def apply(self, rect1, rect2, alignment, padding):
		lx, ly, lwidth, lheight = rect1
		tx, ty, twidth, theight = rect2
		if alignment == Alignment.CENTER:
			x = int(lx + (lwidth - twidth) / 2)
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == Alignment.LEFT:
			x = lx + padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == Alignment.RIGHT:
			x = lx + (lwidth - twidth) - padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y) 
		return (0, 0)
Alignment = Alignment()

class Padding(object):
	def __init__(self):
		pass

	def apply(self, padsize, side=[]):
		pass

class Margin(object):
	def __init__(self):
		pass

	def apply(self):
		pass

"""
	check if rect2 collides with rect1
"""
def CheckCollision(rect1, rect2):
	x1, y1, width1, height1 = rect1
	x2, y2, _, _ = rect2

	if (x2 > x1 and x2 < (x1 + width1)) and (y2 > y1 and y2 < (y1 + height1)):
		return True
	return False

# def EdgeDetector(object):
# 	def __init__(self):
# 		self.currState = 0
# 		self.prevState = 0
# 		(self.unchanging,
# 		 self.falling,
# 		 self.rising) = [i for i in range(0, 2)]
# 		self.state = self.unchanging

# 	def update(self, state):
# 		self.currState = state
# 		if self.currState > self.prevState:

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

class Label(Widget):
	# def __init__(self, text="", textAlignment=Alignment.center, borderVisible=True):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.text = kwargs.get('text', "")
		# self.textColor = WHITE
		self.textColor = tuple([0xff] * 3)
		self.border = 2
		self.borderColor = BLUE

		self.borderVisible = kwargs.get('borderVisible', True)

		# how much room between edge and text (padding between text and label border)
		self.defaultPadding = 8
		self.padding = self.defaultPadding

		self.textAlignment = kwargs.get('textAlignment', Alignment.CENTER)
		self.textSurface, self.textRect = UIFont.render(self.text, self.textColor)
		_, _, textWidth, textHeight = self.textRect
		self.rect = (0, 0, textWidth * 1.5 + self.defaultPadding, textHeight * 1.5 + self.defaultPadding)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			pygame.draw.rect(surface, self.borderColor, self.applyOffset(self.rect), self.border)
	
	def draw(self, surface):
		""" Draw the text after applying a alignment function to its position. """
		x, y = Alignment.apply(self.applyOffset(self.rect), self.textRect, self.textAlignment, self.padding)
		surface.blit(self.textSurface, (x, y))
		""" draw a border """
		self.drawBorder(surface)

class Button(Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.mpos = 0, 0

		""" Custom label properties for a button. """
		self.borderPadding = self.border * 2
		_, _, textWidth, textHeight = self.textRect
		self.rect = (50, 50, textWidth * 1.5 + self.defaultPadding + self.borderPadding + 200, textHeight * 1.5 + self.defaultPadding + self.borderPadding)
		self.borderColor = [169] * 3
		self.textAlignment = Alignment.RIGHT

		self.clickState = 0
		self.prevClickState = 0

		self.onPressed = None
		self.onReleased = None

		self.pressedCallback = None
		self.releasedCallback = None

		"""
			if highLightBorder has a value high then zero an highlight border that size is draw
			if highLightBorder is zero then the rect is filled.

			used for indicating a button is set or pressed down.
		"""
		self.highLightBorder = 0

		self.highLightColor = GREEN
		self.highLightColor = (0, 0xff >> 1, 0)

		self.colliding = False
		self.isHeld = False

	def setClickState(self, clickState):
		self.clickState = clickState

	def isPressed(self):
		return (self.clickState > self.prevClickState)

	def isReleased(self):
		return (self.clickState < self.prevClickState)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			x, y, width, height = self.rect
			smallest = min(width, height)
			marginSize = 10
			marginRect = x + marginSize, y + marginSize, width - marginSize * 2, height - marginSize * 2
			pygame.draw.rect(surface, self.borderColor, self.applyOffset(marginRect), self.border, round(smallest / 3))

	def draw(self, surface):
		""" Draw a highlight when held down. """
		if self.isHeld:
			if(self.borderVisible):
				x, y, width, height = self.rect
				smallest = min(width, height)
				marginSize = 10
				marginRect = x + marginSize, y + marginSize, width - marginSize * 2, height - marginSize * 2
				pygame.draw.rect(surface, self.highLightColor, self.applyOffset(marginRect), self.highLightBorder, round(smallest / 3))

		super().draw(surface)

	def handleEvents(self, event):
		leftMouseBtn, _, _ = pygame.mouse.get_pressed()
		self.setClickState(leftMouseBtn)
		if event.type == pygame.MOUSEMOTION:
			self.mpos = event.pos

	def processEvents(self):
		self.colliding = CheckCollision(self.applyOffset(self.rect), (*self.mpos, 0, 0))
		if self.colliding:
			if self.isPressed():
				self.isHeld = True
				if self.pressedCallback:
					self.pressedCallback(self)
			if self.isReleased():
				if self.releasedCallback:
					self.releasedCallback(self)
		""" update button state when mouse not on it but still releases button """
		if self.isReleased():
			self.isHeld = False
		self.prevClickState = self.clickState

class CheckButton(Button):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.marked = False
		self.prevMarked = False

		self.checkCallback = None
		self.releasedCallback = self.toggleMarked

	def toggleMarked(self, widget):
		self.marked = not self.marked

	def draw(self, surface):
		""" fill in the button if button is set. """
		if(self.marked):
			if(self.borderVisible):
				_, _, width, height = self.rect
				smallest = min(width, height)
				pygame.draw.rect(surface, self.highLightColor, self.applyOffset(self.rect), self.highLightBorder, round(smallest / 3))
		""" Draw the normal border to indicate it's a button. """
		super().draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)

	def processEvents(self):
		super().processEvents()
		if self.prevMarked != self.marked:
			if self.checkCallback:
				self.checkCallback(self)
		self.prevMarked = self.marked

class Indicator(CheckButton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		x, y, width, height = self.rect
		# custom size for testing
		self.rect = x, y + 100, 50, 50

	def setIndicator(self):
		self.marked = True

	def clearIndicator(self):
		self.marked = False

	def handleEvents(self, event):
		pass

	def processEvents(self):
		pass

class Container(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.widgets = []

	def addWidget(self, widget):
		widget.setParent(self)
		self.widgets.append(widget)

	def update(self):
		super().update()
		""" update widget offset relative to the parent """
		for widget in self.widgets:
			x, y, _, _ = self.rect
			widget.setOffset((x, y))
		""" call all update functions for the widgets in this container. """
		for widget in self.widgets:
			widget.update()

	""" Draw all the widgets in the Container. """
	def draw(self, surface):
		self.drawBorder(surface)
		for widget in self.widgets:
			widget.draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)
		for widget in self.widgets:
			widget.handleEvents(event)

	def processEvents(self):
		super().processEvents()
		for widget in self.widgets:
			widget.processEvents()

class Pane(Container):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.borderVisible = True

		self.borderColor = GREEN
		self.border = 1
		self.borderWidth = 1

	def drawBorder(self, surface):
		if self.borderVisible:
			x, y, width, height = self.rect
			rect = x, y, width, height
			# outer border is easy to draw it is just the bounding rectangle.
			pygame.draw.rect(surface, self.borderColor, rect, self.border)
			# calculate inner border and draw it
			inner = x + self.borderWidth + self.border * 2, \
					y + self.borderWidth + self.border * 2, \
					width - (self.borderWidth + self.border * 2) * 2, \
					height - (self.borderWidth + self.border * 2) * 2
			pygame.draw.rect(surface, self.borderColor, inner, self.border, border_radius=10)

class Grid(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.layout = [[]]
		self.rect = (0, 0, 0, 0)

	def addRow(self, widget, pos=0, size=1):
		self.layout[pos].append(widget)

	def addCol(self, widget, pos=0, size=1):
		pass

	def draw(self, surface):
		for row in self.layout:
			for widget in row:
				# set it's position
				widget.draw(surface)

class Box(Container):
	(HORIZONTAL,
	 VERTICAL) = [i for i in range(0, 2)]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.boxType = kwargs.get('type', Box.HORIZONTAL)

	def updateHorizonal(self):
		numWidgets = len(self.widgets)
		x, y, width, height = self.rect
		sectionSize = int(width / numWidgets)
		
		for i, widget in enumerate(self.widgets):
			widgetX, widgetY, widgetWidth, widgetHeight = widget.rect
			widget.rect = x + i * sectionSize, y, sectionSize, height

	def updateVertical(self):
		numWidgets = len(self.widgets)
		x, y, width, height = self.rect
		sectionSize = int(height / numWidgets)
		
		for i, widget in enumerate(self.widgets):
			widgetX, widgetY, widgetWidth, widgetHeight = widget.rect
			widget.rect = x, y + i * sectionSize, width, sectionSize

	def setPosition(self, rect):
		pass

	def setSize(self, rect):
		x, y, width, height = self.rect
		rx, ry, rwidth, rheight = rect
		self.rect = x, y, rwidth, rheight

	def update(self):
		super().update()

		if not len(self.widgets):
			return

		""" update widget size and positions. """
		if self.boxType == Box.HORIZONTAL:
			self.updateHorizonal()
		elif self.boxType == Box.VERTICAL:
			self.updateVertical()

		super().update()

class App(Container):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.Running = True
		self.rect = kwargs.get('rect', (0, 0, *screenSize))

		self.setParent(self) # is this a good idea? this thing is supposed to be the top level

	def update(self):
		for widget in self.widgets:
			widget.setSize(self.rect)
		super().update()

	def quitApplication(self):
		pygame.quit()
		quit()

	def run(self):
		""" update widgets once. """
		self.update()
		""" Run the main loop. """
		while self.Running:
			""" handle all the events. """
			for event in pygame.event.get():
				for widget in self.widgets:
					widget.handleEvents(event)
				""" Exit on pressing escape. """
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.Running = False
				""" Exit on hitting the window X. """
				if event.type == pygame.QUIT:
					self.Running = False
			""" process and draw all the events."""
			screen.fill(BLACK)
			for widget in self.widgets:
				widget.processEvents()
				widget.draw(screen)
			pygame.display.flip()
		self.quitApplication()

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# button = Button(text="Test")
		# button.pressedCallback = self.pressedCallback
		# button.releasedCallback = self.releasedCallback
		# self.addWidget(button)

		# self.indicator = Indicator(text="9000000")
		# self.addWidget(indicator)

		# button = CheckButton(text="Button")
		# button.checkCallback = self.checkCallback
		# self.addWidget(button)
		
		# label = Label("Hello, World!")
		# self.addWidget(label)

		# texts = 	 ["Left", "Center", "Right"]
		# alignments = [Alignment.left, Alignment.center, Alignment.right]
		# for i, (text, alignment) in enumerate(zip(texts, alignments)):
		# 	x = 50
		# 	y = 260 + (i * 60)
		# 	label = Label(text=text, textAlignment=alignment)
		# 	_, _, Lwidth, Lheight = label.rect
		# 	# multiply label width by 2 to exaggerate allignment
		# 	label.rect = x, y, Lwidth * 2, Lheight
		# 	self.addWidget(label)

		# pane = Pane(rect=(0, screenHeight / 2, screenWidth, screenHeight / 2))
		# pane.addWidget(button)
		# pane.addWidget(self.indicator)
		# self.addWidget(pane)
		# print(pane.parent.rect)

		# grid = Grid()
		# for i in range(0, 100):
		# 	grid.addRow(Button(text=f"{i}"))
		# self.addWidget(grid)
		# button = Button(text="Hi")
		# button.pressedCallback = self.pressedCallback
		# self.addWidget(button)

		box = Box(type=Box.VERTICAL)
		box2 = Box(type=Box.HORIZONTAL)
		box2.borderColor = (0xff, 0, 0)
		
		box.addWidget(Widget())
		box.addWidget(Pane())
		box.addWidget(box2)
		box.addWidget(Button())
		box.addWidget(Button())
		box.addWidget(Button())

		box2.id = 42
		box2.addWidget(Pane())
		box2.addWidget(Button())
		# box2.addWidget(Pane())
		# box2.addWidget(Widget())

		# box2.addWidget(Widget())
		# box2.addWidget(Widget())

		self.addWidget(box)

	def checkCallback(self, widget):
		if(widget.marked):
			self.indicator.setIndicator()
		else:
			self.indicator.clearIndicator()
		print(f"checkState: {widget.marked}")

	def pressedCallback(self, widget):
		print(f"pressed {widget} text: {widget.text}")

	def releasedCallback(self, widget):
		print(f"released {widget} text: {widget.text}")

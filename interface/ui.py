import pygame
import pygame.freetype
import time
pygame.init()

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

pygame.font.init()
UIFont = pygame.freetype.Font('resources/fonts/Roboto-Regular.ttf', 18)

class Alignment(object):
	def __init__(self):
		(self.center,
		 self.left,
		 self.right) = [i for i in range(0, 3)]
	"""
		calculate rect2 alignment relative to rect1 with margin
	"""
	def calcAlignment(self, rect1, rect2, alignment, margin):
		lx, ly, lwidth, lheight = rect1
		tx, ty, twidth, theight = rect2
		if alignment == self.center:
			x = int(lx + (lwidth - twidth) / 2)
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == self.left:
			x = lx + margin
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == self.right:
			x = lx + (lwidth - twidth) - margin
			y = int(ly + (lheight - theight) / 2)
			return (x, y) 
		return (0, 0)
Alignment = Alignment()

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
	def __init__(self):
		pass
	""" This function draws the widget """
	def draw(self, surface):
		pass
	""" this function sets the internal state based on outside events."""
	def handleEvents(self, event):
		pass
	""" process previously set state to generate events and call calbacks if needed."""
	def processEvents(self):
		pass

class Label(Widget):
	def __init__(self, text="", textAlignment=Alignment.right):
		super().__init__()
		self.text = text
		self.textColor = GREEN
		self.border = 1
		self.borderColor = BLUE
		self.rect = (50, 50, 150, 50)

		self.textSurface, self.textRect = UIFont.render(self.text, self.textColor)
		self.textAlignment = textAlignment
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.rect, self.border)
		x, y = Alignment.calcAlignment(self.rect, self.textRect, self.textAlignment, 8)
		surface.blit(self.textSurface, (x, y))

"""
	check if rect2 collides with rect1
"""
def CheckCollision(rect1, rect2):
	x1, y1, width1, height1 = rect1
	x2, y2, _, _ = rect2

	if (x2 > x1 and x2 < (x1 + width1)) and (y2 > y1 and y2 < (y1 + height1)):
		return True
	return False

class Button(Widget):
	def __init__(self):
		super().__init__()
		self.borderColor = RED
		self.border = 1
		self.mpos = 0, 0
		self.rect = (100, 150, 100, 100)

		self.state = 0
		self.prevState = 0

		self.onPressed = None
		self.onReleased = None

	def setState(self, state):
		self.state = state

	def draw(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.rect, self.border)
	
	def handleEvents(self, event):
		leftMouseBtn, _, _ = pygame.mouse.get_pressed()
		self.setState(leftMouseBtn)
		if event.type == pygame.MOUSEMOTION:
			self.mpos = event.pos

	def processEvents(self):
		colliding = CheckCollision(self.rect, (*self.mpos, 0, 0))
		if colliding:
			if self.state > self.prevState:
				if self.pressedCallback:
					self.pressedCallback()
				self.border = 10
			if self.state < self.prevState:
				if self.releasedCallback:
					self.releasedCallback()
				self.border = 1
			self.prevState = self.state

		# x, y, width, height = self.rect
		# mx, my = self.mpos

		# if (mx > x and mx < (x + width)) and (my > y and my < (y + height)):
		# 	self.border = 10
		# 	if self.state > self.prevState:
		# 		if self.pressedCallback:
		# 			self.pressedCallback()
		# 	elif self.state < self.prevState:
		# 		if self.releasedCallback:
		# 			self.releasedCallback()
		# 	elif (self.state == self.prevState) and self.state == 1:
		# 		pass
		# 	elif (self.state == self.prevState) and self.state == 0:
		# 		pass
		# else:
		# 	self.border = 1
		# self.prevState = self.state

class App(Widget):
	def __init__(self):
		self.Running = True
		self.widgets = []

	def addWidget(self, widget):
		self.widgets.append(widget)

	def quitApplication(self):
		pygame.quit()
		quit()

	def run(self):
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
			screen.fill(BLACK)
			""" process and draw all the events."""
			for widget in self.widgets:
				widget.processEvents()
				widget.draw(screen)
			pygame.display.flip()
		self.quitApplication()

class TestApp(App):
	def __init__(self):
		super().__init__()
		button = Button()
		button.pressedCallback = self.pressedCallback
		button.releasedCallback = self.releasedCallback
		self.addWidget(button)
		
		label = Label("Hello, World!")
		self.addWidget(label)

		texts = 	 ["Left", "Center", "Right"]
		alignments = [Alignment.left, Alignment.center, Alignment.right]
		for i, (text, alignment) in enumerate(zip(texts, alignments)):
			x = 50
			y = 260 + (i * 60)
			label = Label(text=text, textAlignment=alignment)
			_, _, Lwidth, Lheight = label.rect
			label.rect = x, y, Lwidth, Lheight
			self.addWidget(label)


	def pressedCallback(self):
		print("pressed button.")

	def releasedCallback(self):
		print("released button.")

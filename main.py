from basicparts.Part import Part
from basicparts.Gates import And, Or, Not, Buffer, Nand, Nor, Xor, Xnor
from basicparts.Latch import SRLatch, GatedLatch, DataLatch
from basicparts.FlipFlop import FlipFlop, DFlipFlop, TFlipFlop
from basicparts.Adder import HalfAdder, FullAdder
from basicparts.Mux import Mux, DeMux, TestMux
from basicparts.Encoder import Decoder

from utils.TestUtils import testPart, testFlipFlop
from utils.TestUtils import numToBits, clockPart

from devices.MC14K5 import MC14K5

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
		calcAlignment(): calculate rect2 alignment relative to rect1 with margin
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

class Label(object):
	def __init__(self, text=""):
		self.text = text
		self.textColor = GREEN
		self.border = 1
		self.borderColor = BLUE
		self.rect = (50, 50, 150, 50)

		self.textSurface, self.textRect = UIFont.render(self.text, self.textColor)
		self.alignment = Alignment.right
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.rect, self.border)
		x, y = Alignment.calcAlignment(self.rect, self.textRect, self.alignment, 8)
		surface.blit(self.textSurface, (x, y))

	def handleEvents(self):
		pass

class Button(object):
	def __init__(self):
		self.borderColor = RED
		self.border = 1
		self.mpos = 0, 0
		self.rect = (100, 150, 100, 100)

		self.state = 0
		self.prevState = 0

		self.clickedHandler = None

		self.printed = False

	def setState(self, state):
		self.state = state

	def checkState(self):
		x, y, width, height = self.rect
		mx, my = self.mpos

		if (mx > x and mx < (x + width)) and (my > y and my < (y + height)):
			self.border = 10
			if self.state > self.prevState:
				if self.clickedHandler:
					self.clickedHandler()
			elif self.state < self.prevState:
				pass
			elif (self.state == self.prevState) and self.state == 1:
				pass
			elif (self.state == self.prevState) and self.state == 0:
				pass
		else:
			self.border = 1
		self.prevState = self.state
	def draw(self, surface):
		pygame.draw.rect(surface, self.borderColor, self.rect, self.border)
	def handleEvents(self):
		self.checkState()

def quitApplication():
	pygame.quit()
	quit()

def ClickedCallback():
	global Running
	Running = False
	print(Running)

if __name__ == "__main__":
	button = Button()
	label = Label("Hello, World!")
	button.clickedHandler = ClickedCallback
	while Running:
		screen.fill(BLACK)
		button.handleEvents()
		button.draw(screen)
		label.draw(screen)
		for event in pygame.event.get():
			leftMouseBtn, middleMouseBtn, rightMouseBtn = pygame.mouse.get_pressed()
			button.setState(leftMouseBtn)
			if event.type == pygame.MOUSEMOTION:
				button.mpos = event.pos
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					Running = False
			if event.type == pygame.QUIT:
				Running = False
		pygame.display.flip()
	quitApplication()

if __name__ == "__main__":
	print("Hello, world!")

	testPart(And())
	testPart(Or())
	testPart(Not())
	testPart(Buffer())
	testPart(Nand())
	testPart(Nor())
	testPart(Xor())
	testPart(Xnor())

	testPart(SRLatch())
	testPart(GatedLatch())
	testPart(DataLatch())

	testPart(HalfAdder())
	testPart(FullAdder())

	testFlipFlop(FlipFlop())
	testFlipFlop(DFlipFlop())
	testFlipFlop(TFlipFlop())

	testPart(Decoder())
	TestMux(Mux())
	testPart(DeMux())


	MC14K5.TestLU()


	testPart(MC14K5.Decoder())
	testPart(MC14K5.Mux())
	testPart(MC14K5.InstrDecoder())
	testPart(MC14K5.InstrRegister())
	testFlipFlop(MC14K5.InstrRegister())
	# testPart(MC14K5.ControlUnit())

	instr = MC14K5.Instructions()
	control = MC14K5.ControlUnit()

	print("-> input enable.")
	control.setInput(0, 1, *numToBits(4, instr.IEN))
	clockPart(control)
	print("-> LD(1) and STO(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)
	print("-> LD(0) and STO(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)

	print("-> LD(1) and STOC(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockPart(control)
	print("-> LD(0) and STOC(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockPart(control)

	print("-> output enable.")
	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)


	print("-> write 1 through loading zero and storing the complement.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPO))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPF))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.SKZ))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.RTN))
	clockPart(control)
	
	control.setInput(0, 1, *numToBits(4, instr.JMP))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.STO))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)


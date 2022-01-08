import pygame
import pygame.freetype
import time

from interface.window import App
from interface.widget import Widget
from interface.label import Label
from interface.button import CheckButton
from interface.button import Button
from interface.container import Box
from interface.container import Pane
from interface.container import Grid
from interface.container import Container
from interface.alignment import Alignment

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
		box.addWidget(box2)
		box.addWidget(Pane())
		box.addWidget(Button())
		box.addWidget(Button())
		box.addWidget(Button())

		box2.id = 42
		box2.addWidget(Button(text="1", textAlignment=Alignment.CENTER))
		box2.addWidget(Button(text="2", textAlignment=Alignment.CENTER))
		box2.addWidget(Button(text="3", textAlignment=Alignment.CENTER))
		box2.addWidget(Pane())
		# box2.addWidget(Label())
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

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
from interface.container import PackedBox

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





		# box = Box(type=Box.VERTICAL)
		# box2 = Box(type=Box.HORIZONTAL)
		# box2.borderColor = (0xff, 0, 0)
		
		# # box.addWidget(Widget())
		# box.addWidget(Button())
		# box.addWidget(box2)
		# box.addWidget(Button())
		# box.addWidget(Button())
		# box.addWidget(Button())
		# newBox = Box()
		# newBox.addWidget(Label(text="label 1"))
		# newBox.addWidget(CheckButton(text="CheckButton"))
		# newBox.addWidget(Button(text="But no"))
		# box.addWidget(newBox)
		# box.addWidget(Label(text="Hello, World!"))

		# box2.id = 42
		# box2.addWidget(Button(text="1"))
		# box2.addWidget(Button(text="2"))
		# box2.addWidget(Button(text="3"))
		# pane = Pane()
		# pane.addWidget(Button())
		# box2.addWidget(pane)
		# # box2.addWidget(Grid())
		# box2.addWidget(Box())
		# # box2.addWidget(Container())
		# # box2.addWidget(Label(text="ABC"))
		# box2.addWidget(Widget())

		# # box2.addWidget(Widget())
		# # box2.addWidget(Widget())

		# self.addWidget(box)



		# label = Label(text="A line of Text but longer A line of Text", behaviour=Widget.FIXED)
		# label.setPosition((200, 200))
		# self.addWidget(label)

		# widget = Widget(behaviour=Widget.FIXED)
		# widget.setPosition((200, 200))
		# self.addWidget(widget)

		# container = Box(type=Box.VERTICAL)
		# container2 = Box(type=Box.HORIZONTAL)
		# container2.setPosition((200, 200))
		# container2.addWidget(Container())
		# container2.addWidget(Label(text="label", textAlign=Alignment.RIGHT))
		# container2.addWidget(Button(text="Hello"))
		# container2.addWidget(CheckButton(text="Hello"))
		# container2.addWidget(Pane())
		# container.addWidget(container2)
		# container.addWidget(Container())
		# container.addWidget(Label(text="box", textAlign=Alignment.LEFT))
		# container.addWidget(Button(text="box"))
		# container.addWidget(CheckButton(text="original"))
		# container.addWidget(Pane())
		# self.addWidget(container)

		# container = PackedBox(type=PackedBox.VERTICAL)
		# self.addWidget(container)
		# widget = Widget(behaviour=Widget.FILL)

		# box = Box(type=Box.HORIZONTAL)
		# b2 = Box(type=Box.VERTICAL)
		# b2.addWidget(Widget())
		# b2.addWidget(Widget())
		# box.addWidget(b2)
		# box.addWidget(Widget(behaviour=Widget.EXPAND))
		# self.addWidget(box)

		from devices.MC14K5.MC14K5 import LogicUnit
		
		vbox = Box(type=Box.VERTICAL)
		self.addWidget(vbox)

		hbox0 = Box(type=Box.HORIZONTAL)
		hbox1 = Box(type=Box.HORIZONTAL)
		hbox2 = Box(type=Box.HORIZONTAL)
		hbox3 = Box(type=Box.HORIZONTAL)
		vbox.addWidget(hbox0)
		vbox.addWidget(hbox1)
		vbox.addWidget(hbox2)
		# vbox.addWidget(hbox3)

		logicUnit = LogicUnit()
		deviceName = Label(text=logicUnit.name, behaviour=Widget.FIXED)
		hbox0.addWidget(deviceName)
		self.addInput(hbox1, logicUnit.Data, "Data")
	
	def addInput(self, box, input, text):
		checkbutton = CheckButton(text=text)
		checkbutton.checkCallback = self.setLogic
		checkbutton.id = input
		box.addWidget(checkbutton)
	
	def setLogic(self, widget):
		print(type(widget.id))
		widget.id = 42

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

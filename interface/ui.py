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
		self.node = lambda : 0

	def setIndicator(self):
		self.marked = True

	def clearIndicator(self):
		self.marked = False
	
	"""
		watch node keeps track of the state of node
		node should be a reference so that it can be called to give back a 1/0 value
		when called
	"""
	def Watch(self, node):
		self.node = node

	def processWatch(self):
		self.marked = self.node()

	def handleEvents(self, event):
		pass

	def processEvents(self):
		self.processWatch()

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		from basicparts.Gates import And
		self.gate = And()

		# vbox = Box(type=Box.VERTICAL)
		# self.addWidget(vbox)

		# vbox.addWidget(Label(text=self.gate.name))
		
		# hbox1 = Box(type=Box.HORIZONTAL)
		# vbox.addWidget(hbox1)

		# output = Indicator()
		# vbox.addWidget(output)

		# input1 = CheckButton(text=self.gate.lines[0])
		# input2 = CheckButton(text=self.gate.lines[1])
		# hbox1.addWidget(input1)
		# hbox1.addWidget(input2)

		# input1.checkCallback = self.setInput1
		# input2.checkCallback = self.setInput2
		# output.Watch(self.gate.Q)

		""" Basic Layout. """
		partbox   = Box(type=Box.VERTICAL)
		namebox   = Box(type=Box.HORIZONTAL)
		inputbox  = Box(type=Box.HORIZONTAL)
		outputbox = Box(type=Box.HORIZONTAL)

		partbox.addWidget(namebox)
		partbox.addWidget(inputbox)
		partbox.addWidget(outputbox)
		self.addWidget(partbox)

		""" add name label. """
		namebox.addWidget(Label(text=self.gate.name))

		""" add the inputs. """
		for input in self.gate.inputs:
			inputbox.addWidget(CheckButton())

		""" add the outputs. """
		for output in self.gate.outputs:
			outputbox.addWidget(Indicator())
	
	def processEvents(self):
		# self.gate.process()
		pass

	def setInput1(self, widget):
		value = 1 if widget.marked else 0
		self.gate.A(value)

	def setInput2(self, widget):
		value = 1 if widget.marked else 0
		self.gate.B(value)

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

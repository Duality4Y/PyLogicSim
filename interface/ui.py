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

from interface.colorDefs import *

class Padding(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.visible = False
	

class Indicator(CheckButton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.node = lambda : 0

	def setIndicator(self):
		self.marked = True

	def clearIndicator(self):
		self.marked = False
	
	"""
		watch sets a internal reference to a 'node'
		a 'node' is just a reference to a function which returns
		boolean like value which can be used to set the state of the indicator.
	"""
	def watch(self, node):
		self.node = node

	def processWatch(self):
		self.marked = 1 if self.node() else 0

	def handleEvents(self, event):
		pass

	def processEvents(self):
		self.processWatch()


from basicparts.Gates import Nand, Not, Buffer
from devices.MC14K5.MC14K5 import ControlUnit
from devices.MC14K5.MC14K5 import Instructions
from utils.TestUtils import numToBits

class InstrSelectBox(Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, type=Box.HORIZONTAL)
		self.part = kwargs.get("part")

		self.instructions = Instructions()
		instrNames = [attr for attr in dir(self.instructions) if not callable(getattr(self.instructions, attr)) and not attr.startswith("__")]
		self.instrInputs = (self.part.I3, self.part.I2, self.part.I1, self.part.I0)
		
		self.prevCheckedButton = None

		for instrName in instrNames:
			checkButton = Button(text=instrName)
			checkButton.releasedCallback = (self.setInstruction, getattr(self.instructions, instrName))
			self.addWidget(checkButton)
	
	def setInstruction(self, w, instrValue):
		instrBits = numToBits(4, instrValue)
		for value, input in zip(instrBits, self.instrInputs):
			input(value)

class PartControlBox(Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, type=Box.VERTICAL)
		self.part = kwargs.get("part", Nand())

		""" setup the basic layout."""
		self.nameLabel = Label(text=self.part.name)
		self.inputBox = Box(type=Box.HORIZONTAL)
		self.outputBox = Box(type=Box.HORIZONTAL)
		self.addWidget(self.nameLabel)
		self.addWidget(self.inputBox)
		self.addWidget(self.outputBox)

		""" 
			Add inputs to the input box
			connect them through a callback to the part inputs.
		"""
		for input in self.part.inputs:
			checkButton = CheckButton(text=input.__name__)
			checkButton.checkCallback = (self.controlInput, input)
			self.inputBox.addWidget(checkButton)
		
		""" Connect part outputs to indicator and add to layout. """
		for output in self.part.outputs:
			indicator = Indicator(text=output.__name__)
			indicator.watch(output)
			self.outputBox.addWidget(indicator)

	"""
		This callback is called when the button is marked.
		It gets passed the widget that got marked and an extra user argument.
		the extra argument in this case is a 'input' function allowing
		a specific input from a part to be set with a specific CheckBox.
	"""
	def controlInput(self, widget, input):
		value = 1 if widget.marked else 0
		input(value)

	"""
		Do general Event Processing but also Process part.
		Essentially calling part.process() allows the part to update it's internal
		State based on it's current inputs.
		Basically the part processes it's input events.
	"""
	def processEvents(self):
		super().processEvents()
		self.part.process()

class PartDisplayBox(Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, type=Box.VERTICAL)
		self.part = kwargs.get("part", Nand())
		self.title = kwargs.get("title", "None")

		self.titleLabel = Label(text=self.title)
		self.inputBox = Box(type=Box.HORIZONTAL)
		self.outputBox = Box(type=Box.HORIZONTAL)
		self.addWidget(self.titleLabel)
		self.addWidget(self.inputBox)
		self.addWidget(self.outputBox)

		self.titleLabel.borderVisible = False
		self.inputBox.borderVisible = False
		self.outputBox.borderVisible = False

		self.borderColor = (0x80, 0, 0x80)
		self.outputColor = (0x00, 0x70, 0x00)
		self.inputColor = (0x11, 0x8A, 0x11)
		self.clkColor = (0x00, 0x1F, 0x65)
		
		for input in self.part.inputs:
			indicator = Indicator(text=input.__name__)
			print(input.__name__)
			if input.__name__ == "Clk":
				indicator.selectedColor = self.clkColor
			else:
				indicator.selectedColor = self.inputColor
			indicator.watch(input)
			indicator.borderVisible = False
			self.inputBox.addWidget(indicator)

		for output in self.part.outputs:
			indicator = Indicator(text=output.__name__)
			indicator.selectedColor = self.outputColor
			indicator.watch(output)
			indicator.borderVisible = False
			self.outputBox.addWidget(indicator)
		
	def processEvents(self):
		super().processEvents()
		self.part.process()
		

class MC14K5Widget(Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, type=Box.HORIZONTAL)
		self.part = ControlUnit()

		self.partBox = Box(type=Box.VERTICAL)
		self.subPartBox = Box(type=Box.VERTICAL)

		partControlBox = PartControlBox(part=self.part)
		partControlBox.addWidget(InstrSelectBox(part=self.part))
		self.partBox.addWidget(partControlBox)
		self.partBox.addWidget(Box())
		
		self.addWidget(self.partBox)
		self.addWidget(self.subPartBox)
		# self.addWidget(Box())
		
		rowBox = Box(type=Box.HORIZONTAL)
		rowBox.addWidget(PartDisplayBox(part=self.part.JmpLatch, title="JmpLatch"))
		rowBox.addWidget(PartDisplayBox(part=self.part.RtnLatch, title="RtnLatch"))
		rowBox.addWidget(PartDisplayBox(part=self.part.FlagOLatch, title="FlagOLatch"))
		rowBox.addWidget(PartDisplayBox(part=self.part.FlagFLatch, title="FlagFLatch"))
		rowBox.addWidget(PartDisplayBox(part=self.part.SkipLatch, title="SkipLatch"))
		self.subPartBox.addWidget(rowBox)

		rowBox = Box(type=Box.HORIZONTAL)
		rowBox.addWidget(PartDisplayBox(part=self.part.DataInRegister, title="DataInRegister"))
		rowBox.addWidget(PartDisplayBox(part=self.part.DataOutRegister, title="DataOutRegister"))
		rowBox.addWidget(PartDisplayBox(part=self.part.ResultRegister, title="ResultRegister"))
		rowBox.addWidget(PartDisplayBox(part=self.part.mux, title="mux"))
		self.subPartBox.addWidget(rowBox)

		self.subPartBox.addWidget(PartDisplayBox(part=self.part.InstrRegister, title="InstrRegister"))
		self.subPartBox.addWidget(PartDisplayBox(part=self.part.instrDecoder, title="instrDecoder"))
		self.subPartBox.addWidget(PartDisplayBox(part=self.part.logicUnit, title="logicUnit"))
		

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# self.addWidget(PartBox(part=ControlUnit()))
		self.addWidget(MC14K5Widget())
from interface.container import Box
from interface.button import Button
from devices.MC14K5.MC14K5 import ControlUnit
from devices.MC14K5.MC14K5 import Instructions
from partWidgets.widgets import PartControlBox
from partWidgets.widgets import PartDisplayBox

from utils.bitUtils import numToBits

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

class MC14K5ControlMenu(Box):
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

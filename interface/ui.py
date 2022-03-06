from interface.window import App
from interface.colorDefs import *
from partWidgets.widgets import ClockControlWidget
from devices.MC14K5.MC14K5Widgets import MC14K5ControlMenu
from partWidgets.widgets import PartDisplayBox
from basicparts.Counter import NibbleCounter, ByteCounter
from interface.container import Box
from basicparts.Part import Part
from utils.bitUtils import numToBits

class FMemory(Part):
	def __init__(self, addrWidth=13, dataWidth=8):
		super().__init__(name="Memory")
		self.dataList = {}
		self.address = 0
		self.data = 0
		self.size = 2 ** addrWidth

		self.dataWidth = dataWidth
		self.addrWidth = addrWidth

		self.dataFuncBitPos = {}
		self.addrFuncBitPos = {}

		for addr in range(0, self.size):
			self.dataList[addr] = 0
		
		for i in range(0, addrWidth)[::-1]:
			addrFuncStr = f"A{i}"
			addrFunc = getattr(self, addrFuncStr)
			self.addInput(addrFunc, name=addrFuncStr)
			self.addrFuncBitPos[addrFuncStr] = i

		for i in range(0, dataWidth)[::-1]:
			dataFuncStr = f"D{i}"
			dataFunc = getattr(self, dataFuncStr)
			self.addInputOutput(dataFunc, name=dataFuncStr)
			self.dataFuncBitPos[dataFuncStr] = i
	
	def setInput(self, addrBits, dataBits=None):

		for i, v in enumerate(addrBits[::-1]):
			addrFuncStr = f"A{i}"
			addrFunc = getattr(self, addrFuncStr)
			addrFunc(v)

		if dataBits:
			for i, v in enumerate(dataBits[::-1]):
				dataFuncStr = f"D{i}"
				dataFunc = getattr(self, dataFuncStr)
				dataFunc(v)
	
	def __getattr__(self, name):
		def addrBit(*args):
			bit = self.addrFuncBitPos[addrBit.__name__]
			if args:
				if args[0]:
					self.address |= (1 << bit)
				else:
					self.address &= ~(1 << bit)
			return 1 if self.address & (1 << bit) else 0

		def dataBit(*args):
			bit = self.dataFuncBitPos[dataBit.__name__]
			self.data = self.dataList[self.address]
			if args:
				if args[0]:
					self.data |= (1 << bit)
				else:
					self.data &= ~(1<< bit)
				self.dataList[self.address] = self.data
			return 1 if self.data & (1 << bit) else 0
		
		if name.startswith('D'):
			dataBit.__name__ = name
			dataBit.__qualname__ = __class__.__qualname__ + '.' + name
			return dataBit
		elif name.startswith('A'):
			addrBit.__name__ = name
			addrBit.__qualname__ = __class__.__qualname__ + '.' + name
			return addrBit
		
		return object.__getattribute__(self, name)

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		memory = FMemory()
		print(memory.lineTable)
		print(memory)
		
		dataBits = numToBits(8, 0x0F)
		addrBits = numToBits(12, 1024)
		memory.setInput(addrBits, dataBits)
		print(memory)

		addrBits = numToBits(12, 1025)
		memory.setInput(addrBits)
		print(memory)
		
		exit()


		# counter = NibbleCounter()
		# counter = ByteCounter()
		# clockControl = ClockControlWidget()
		# partDisplayBox = PartDisplayBox(part=counter, title="Counter")

		# clockControl.connectClock(counter.Clk)

		# box = Box(behaviour=Box.HORIZONTAL)
		# box.addWidget(clockControl)
		# box.addWidget(partDisplayBox)
		# self.addWidget(box)


		# self.addWidget(MC14K5ControlMenu())


		# clockControlWidget = ClockControlWidget()
		# clockControlWidget.connectClock(self.outputWireTest)
		# self.addWidget(clockControlWidget)
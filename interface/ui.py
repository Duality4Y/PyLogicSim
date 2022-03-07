from interface.window import App
from interface.colorDefs import *
from partWidgets.widgets import ClockControlWidget
from devices.MC14K5.MC14K5Widgets import MC14K5ControlMenu
from partWidgets.widgets import PartDisplayBox, PartControlBox
from basicparts.Counter import NibbleCounter, ByteCounter
from interface.container import Box
from basicparts.Part import Part
from utils.bitUtils import numToBits
from basicparts.Memory import FMemory

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		memory = FMemory()
		print(memory.lineTable)
		
		dataBits = numToBits(8, 0x0F)
		addrBits = numToBits(12, 1024)
		memory.setInput(addrBits, dataBits)
		memory.WE(0)
		memory.process()
		print(memory)

		addrBits = numToBits(12, 1025)
		memory.setInput(addrBits)
		memory.WE(1)
		memory.process()
		print(memory)
		
		dataBits = numToBits(8, 0x0F)
		addrBits = numToBits(12, 10)
		memory.setInput(addrBits, dataBits)
		memory.WE(0)
		memory.process()
		print(memory)

		addrBits = numToBits(12, 11)
		memory.setInput(addrBits)
		memory.WE(1)
		memory.process()
		print(memory)

		addrBits = numToBits(12, 10)
		memory.setInput(addrBits)
		memory.WE(1)
		memory.process()
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
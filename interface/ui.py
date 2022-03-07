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
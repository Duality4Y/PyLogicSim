from interface.window import App
from interface.colorDefs import *
from partWidgets.widgets import ClockControlWidget
from devices.MC14K5.MC14K5Widgets import MC14K5ControlMenu

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# self.addWidget(MC14K5ControlMenu())

		# clockControlWidget = ClockControlWidget()
		# clockControlWidget.connectClock(self.outputWireTest)
		# self.addWidget(clockControlWidget)
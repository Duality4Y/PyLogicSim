from basicparts.Gates import Nand
from interface.label import Label
from interface.button import CheckButton, Button
from interface.container import Box

from utils.timer import TimedEvent

"""
	Clock Control widget allow automatic clocking
	or step wise clocking by pressing a button.
"""
class ClockControlWidget(Box):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs, type=Box.VERTICAL)

		self.clockState = False

		self.nameLabel = Label(text="Clock Control")
		self.controlBox = Box(type=Box.HORIZONTAL)
		
		self.stepButton = Button(text="Step")
		self.enableClockButton = CheckButton(text="Enable Clock")
		self.controlBox.addWidget(self.stepButton)
		self.controlBox.addWidget(self.enableClockButton)

		self.clockIndicator = Indicator(text="Clock State")
		
		self.addWidget(self.nameLabel)
		self.addWidget(self.controlBox)
		self.addWidget(self.clockIndicator)

		self.stepButton.pressedCallback = self.startStepTimedEvent, None
		self.enableClockButton.checkCallback = self.startClockTimedEvent, None
		self.clockIndicator.watch(self.getClockState)

		self.clockTimedEvent = TimedEvent()

		self.outputWire = None
	
	def connectClock(self, wire):
		self.outputWire = wire
	
	""" Returns the current state of the clock as a integer used in indicator to show the state. """
	def getClockState(self):
		return 1 if self.clockState else 0
	
	""" set timer callback for a single pulse and start the timer. """
	def startStepTimedEvent(self, widget, arg):
		self.clockTimedEvent.callback = self.pulseStepCallback
		self.clockTimedEvent.start()
	
	"""
		Callback inverts the clock state and then returns the state of that clock.
		in the first cycle the clock will be true allowing the timer to run again
		in the second cycle the clock will be false disabling the timer
		after which a full cycle of the clock is completed.
	"""
	def pulseStepCallback(self):
		self.clockState = not self.clockState
		return self.clockState

	""" set timer callback for a continues pulse and start the timer. """
	def startClockTimedEvent(self, widget, arg):
		self.clockTimedEvent.callback = self.pulseClockCallback
		self.clockTimedEvent.start()

	"""
		Clocks for as long as the checkbutton is marked or if the clock is high
		this so that the clock always ends up being false or low.
	"""
	def pulseClockCallback(self):
		self.clockState = not self.clockState
		return self.enableClockButton.marked or self.clockState
	
	def processEvents(self):
		super().processEvents()
		self.clockTimedEvent.processEvents()

		if self.outputWire:
			self.outputWire(self.getClockState())
	
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
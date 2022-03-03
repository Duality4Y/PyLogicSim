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

class TimedEvent(object):
	def __init__(self):
		self.nextTime = 0
		self.interval = 1

		self.callback = None
		self.stop()

	""" set next time to trigger at. """
	def setNextTime(self):
			self.nextTime = time.time() + self.interval
	
	""" staring is simply setting the next time. """
	def start(self):
		self.setNextTime()
	
	""" stoping is simply making the next time negative. """
	def stop(self):
		self.nextTime = -1
	
	""" 
		the callback is called every time a interval of time passes.
		and the next time is set if it returns a true value
		other wise it will stop the timer.

		this allows callbacks to determine when the timer should stop
		for example after X ticks or other use cases.
	"""
	def processEvents(self):
		if self.nextTime < 0:
			return
		
		if time.time() > self.nextTime:
			if self.callback:
				if self.callback():
					self.setNextTime()
				else:
					self.stop()


	
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

from devices.MC14K5.widgets import MC14K5Widget

class TestApp(App):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# self.addWidget(PartBox(part=ControlUnit()))
		# self.addWidget(MC14K5Widget())

		self.addWidget(ClockControlWidget())
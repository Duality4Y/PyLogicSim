import time

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
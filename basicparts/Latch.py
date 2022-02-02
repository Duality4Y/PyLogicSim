from basicparts.Part import Part
from basicparts.Gates import Nor, And, Not

class SRLatch(Part):
	def __init__(self):
		super().__init__(name=SRLatch.__name__)

		self.nor1 = Nor()
		self.nor2 = Nor()

		self.addInput(self.Reset)
		self.addInput(self.Set)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)

		# Cheeky way to force output to zero and input to zero.
		# normal latches do not work like this.
		self.Reset(0)
		self.Set(0)
		self.Q(0)
		self.Qn(0)
		self.process()

	def Set(self, *args):
		if args: self.nor2.B(*args)
		return self.nor2.B()
	
	def Reset(self, *args):
		if args: self.nor1.A(*args)
		return self.nor1.A()
	
	def Q(self, *args):
		if args: self.nor1.Q(*args)
		return self.nor1.Q()

	def Qn(self, *args):
		if args: self.nor2.Q(*args)
		return self.nor2.Q()

	def setInput(self, Reset, Set):
		self.Reset(Reset)
		self.Set(Set)

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.nor1.setInput(self.Reset(), self.Qn())
		self.nor2.setInput(self.Q(), self.Set())
		self.nor1.process()
		self.nor2.process()

		self.nor1.setInput(self.Reset(), self.Qn())
		self.nor2.setInput(self.Q(), self.Set())
		self.nor1.process()
		self.nor2.process()

class GatedLatch(Part):
	def __init__(self):
		super().__init__(name=GatedLatch.__name__)
		self.latch = SRLatch()
		self.and1 = And()
		self.and2 = And()

		self.addInput(self.Clk)
		self.addInput(self.Reset)
		self.addInput(self.Set)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)

	def Clk(self, *args):
		if args:
			self.and1.B(*args)
			self.and2.A(*args)
		return self.and1.B()

	def Reset(self, *args):
		if args: self.and1.A(*args)
		return self.and1.A()

	def Set(self, *args):
		if args: self.and2.B(*args)
		return self.and2.B()

	def Q(self, *args):
		if args: self.latch.Q(*args)
		return self.latch.Q()

	def Qn(self, *args):
		if args: self.latch.Qn(*args)
		return self.latch.Qn()

	def setInput(self, Clk, Reset, Set):
		self.Clk(Clk)
		self.Reset(Reset)
		self.Set(Set)

	def getOutput(self):
		return (self.Q(), self.Qn())

	def process(self):
		self.and1.process()
		self.and2.process()

		self.latch.Reset(self.and1.Q())
		self.latch.Set(self.and2.Q())
		self.latch.process()

class DataLatch(Part):
	def __init__(self):
		super().__init__(name=DataLatch.__name__)

		self.latch = GatedLatch()
		self.notGate = Not()

		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)
	
	def Clk(self, *args):
		if args: self.latch.Clk(*args)
		return self.latch.Clk()
	
	def Data(self, *args):
		if args: self.notGate.A(*args)
		return self.notGate.A()
	
	def Q(self, *args):
		if args: self.latch.Q(*args)
		return self.latch.Q()
	
	def Qn(self, *args):
		if args: self.latch.Qn(*args)
		return self.latch.Qn()

	def setInput(self, Clk, Data):
		self.Clk(Clk)
		self.Data(Data)

	def getOutput(self):
		return (self.Q(), self.Qn())

	def process(self):
		self.notGate.process()

		self.latch.Reset(self.notGate.Q())
		self.latch.Set(self.notGate.A())
		self.latch.process()
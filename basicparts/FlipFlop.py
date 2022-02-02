from basicparts.Part import Part
from basicparts.Gates import Not
from basicparts.Latch import GatedLatch

class FlipFlop(Part):
	def __init__(self):
		super().__init__(name=FlipFlop.__name__)
		
		self.notGate = Not()
		self.masterLatch = GatedLatch()
		self.slaveLatch = GatedLatch()
		
		self.addInput(self.Clk)
		self.addInput(self.Reset)
		self.addInput(self.Set)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)

	def Clk(self, *args):
		self.notGate.A(*args)
		return self.masterLatch.Clk(*args)

	def Reset(self, *args):
		return self.masterLatch.Reset(*args)
	
	def Set(self, *args):
		return self.masterLatch.Set(*args)

	def Q(self, *args):
		return self.slaveLatch.Qn(*args)
	
	def Qn(self, *args):
		return self.slaveLatch.Q(*args)

	def setInput(self, Clk, Reset, Set):
		# print(Clk, Reset, Set)
		self.Clk(Clk)
		self.Reset(Reset)
		self.Set(Set)

	def getOutput(self):
		return (self.Q(), self.Qn())

	def process(self):
		self.masterLatch.process()
		self.notGate.process()

		self.slaveLatch.Reset(self.masterLatch.Q())
		self.slaveLatch.Set(self.masterLatch.Qn())
		self.slaveLatch.Clk(self.notGate.Q())
		self.slaveLatch.process()

class DFlipFlop(Part):
	def __init__(self):
		super().__init__(name=DFlipFlop.__name__)
		
		self.notGate = Not()
		self.notGate2 = Not()
		self.masterLatch = GatedLatch()
		self.slaveLatch = GatedLatch()

		# set initial state Q to zero
		self.Data(0)
		self.Clk(1)
		self.process()
		self.Clk(0)
		self.process()

		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)
	
	def Clk(self, *args):
		self.masterLatch.Clk(*args)
		return self.notGate.A(*args)
	
	def Data(self, *args):
		self.masterLatch.Reset(*args)
		return self.notGate2.A(*args)
	
	def Q(self, *args):
		return self.slaveLatch.Q(*args)
	
	def Qn(self, *args):
		return self.slaveLatch.Qn(*args)

	def setInput(self, Clk, Data):
		self.Clk(Clk)
		self.Data(Data)

	def getOutput(self):
		return (self.Q(), self.Qn())

	def process(self):
		self.notGate2.process()

		self.masterLatch.Set(self.notGate2.Q())
		self.masterLatch.process()
		
		self.notGate.process()

		self.slaveLatch.Reset(self.masterLatch.Q())
		self.slaveLatch.Set(self.masterLatch.Qn())
		self.slaveLatch.Clk(self.notGate.Q())
		self.slaveLatch.process()

class TFlipFlop(Part):
	def __init__(self):
		super().__init__(name=TFlipFlop.__name__)
		
		self.dFlipFlop = DFlipFlop()

		self.addInput(self.T)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)
	
	def T(self, *args):
		return self.dFlipFlop.Clk(*args)

	def Q(self, *args):
		return self.dFlipFlop.Q(*args)
	
	def Qn(self, *args):
		return self.dFlipFlop.Qn(*args)

	def setInput(self, T):
		self.T(T)

	def getOutput(self):
		return (self.Q(), self.Qn())

	def process(self):
		self.dFlipFlop.Data(self.dFlipFlop.Qn())
		self.dFlipFlop.process()

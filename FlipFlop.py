from Part import Part
from Gates import Not
from Latch import GatedLatch

class FlipFlop(Part):
	def __init__(self):
		self.notGate = Not()
		self.masterLatch = GatedLatch()
		self.slaveLatch = GatedLatch()
		
		super().__init__(numInputs=3, numOutputs=2,
						 name=FlipFlop.__name__,
						 lines=["Clk", "Reset", "Set", "Q", "Qn"])
	
	@property
	def Clk(self):
		return self.masterLatch.Clk
	@Clk.setter
	def Clk(self, value):
		self.masterLatch.Clk = value
		self.notGate.A = value

	@property
	def Reset(self):
		return self.masterLatch.Reset
	@Reset.setter
	def Reset(self, value):
		self.masterLatch.Reset = value

	@property
	def Set(self):
		return self.masterLatch.Set
	@Set.setter
	def Set(self, value):
		self.masterLatch.Set = value

	@property
	def Q(self):
		return self.slaveLatch.Qn
	@property
	def Qn(self):
		return self.slaveLatch.Q

	def setInput(self, Clk, Reset, Set):
		# print(Clk, Reset, Set)
		self.Clk = Clk
		self.Reset = Reset
		self.Set = Set

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.masterLatch.process()
		self.notGate.process()

		self.slaveLatch.Reset = self.masterLatch.Q
		self.slaveLatch.Set = self.masterLatch.Qn
		self.slaveLatch.Clk = self.notGate.Q
		self.slaveLatch.process()

	def __repr__(self):
		states = [self.Clk, self.Reset, self.Set, self.Q, self.Qn]
		return self.buildTable(states)

class DFlipFlop(Part):
	def __init__(self):
		self.notGate = Not()
		self.notGate2 = Not()
		self.masterLatch = GatedLatch()
		self.slaveLatch = GatedLatch()

		# set initial state Q to zero
		self.Data = 0
		self.Clk = 1
		self.process()
		self.Clk = 0
		self.process()

		super().__init__(numInputs=2, numOutputs=2,
						 name=FlipFlop.__name__,
						 lines=["Clk", "Data", "Q", "Qn"])
	
	@property
	def Clk(self):
		return self.masterLatch.Clk
	@Clk.setter
	def Clk(self, value):
		self.masterLatch.Clk = value
		self.notGate.A = value

	@property
	def Data(self):
		return self.masterLatch.Reset
	@Data.setter
	def Data(self, value):
		self.masterLatch.Reset = value
		self.notGate2.A = value

	@property
	def Q(self):
		return self.slaveLatch.Q
	@property
	def Qn(self):
		return self.slaveLatch.Qn

	def setInput(self, Clk, Data):
		self.Clk = Clk
		self.Data = Data

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.notGate2.process()

		self.masterLatch.Set = self.notGate2.Q
		self.masterLatch.process()
		
		self.notGate.process()

		self.slaveLatch.Reset = self.masterLatch.Q
		self.slaveLatch.Set = self.masterLatch.Qn
		self.slaveLatch.Clk = self.notGate.Q
		self.slaveLatch.process()

	def __repr__(self):
		states = [self.Clk, self.Data, self.Q, self.Qn]
		return self.buildTable(states)
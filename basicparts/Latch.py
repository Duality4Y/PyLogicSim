from basicparts.Part import Part
from basicparts.Gates import Nor, And, Not

class SRLatch(Part):
	def __init__(self):
		self.nor1 = Nor()
		self.nor2 = Nor()

		# force initial state of zero for Q
		self.setInput(1, 0)
		self.process()

		super().__init__(numInputs=2, numOutputs=2,
						 name=SRLatch.__name__,
						 lines=["Reset", "Set", "Q", "Qn"])

	@property
	def Set(self):
		return self.nor2.B
	@Set.setter
	def Set(self, value):
		self.nor2.B = value

	@property
	def Reset(self):
		return self.nor1.A
	@Reset.setter
	def Reset(self, value):
		self.nor1.A = value

	@property
	def Q(self):
		return self.nor1.Q

	@property
	def Qn(self):
		return self.nor2.Q

	def setInput(self, Reset, Set):
		self.Reset = Reset
		self.Set = Set

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.nor1.setInput(self.Reset, self.Qn)
		self.nor2.setInput(self.Q, self.Set)
		self.nor1.process()
		self.nor2.process()
		# print(f"{self.Q = }")

		self.nor1.setInput(self.Reset, self.Qn)
		self.nor2.setInput(self.Q, self.Set)
		self.nor1.process()
		self.nor2.process()
		# print(f"{self.Q = }")

	def __repr__(self):
		states = [self.Reset, self.Set, self.Q, self.Qn]
		return self.buildTable(states)

class GatedLatch(Part):
	def __init__(self):
		self.latch = SRLatch()
		self.and1 = And()
		self.and2 = And()

		super().__init__(numInputs=3, numOutputs=2,
						 name=GatedLatch.__name__,
						 lines=["Clk", "Reset", "Set", "Q", "Qn"])

	@property
	def Clk(self):
		return self.and1.B
	@Clk.setter
	def Clk(self, value):
		self.and1.B = value
		self.and2.A = value

	@property
	def Reset(self):
		return self.and1.A
	@Reset.setter
	def Reset(self, value):
		self.and1.A = value

	@property
	def Set(self):
		return self.and2.B
	@Set.setter
	def Set(self, value):
		self.and2.B = value

	@property
	def Q(self):
		return self.latch.Q
	@property
	def Qn(self):
		return self.latch.Qn

	def setInput(self, Clk, Reset, Set):
		self.Clk = Clk
		self.Reset = Reset
		self.Set = Set

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.and1.process()
		self.and2.process()

		self.latch.Reset = self.and1.Q
		self.latch.Set = self.and2.Q
		self.latch.process()

	def __repr__(self):
		states = [self.Clk, self.Reset, self.Set, self.Q, self.Qn]
		return self.buildTable(states)

class DataLatch(Part):
	def __init__(self):
		self.latch = GatedLatch()
		self.notGate = Not()

		super().__init__(numInputs=2, numOutputs=2,
						 name=DataLatch.__name__,
						 lines=["Clk", "Data", "Q", "Qn"])

	@property
	def Clk(self):
		return self.latch.Clk

	@Clk.setter
	def Clk(self, value):
		self.latch.Clk = value

	@property
	def Data(self):
		return self.notGate.A

	@Data.setter
	def Data(self, value):
		self.notGate.A = value

	@property
	def Q(self):
		return self.latch.Q

	@property
	def Qn(self):
		return self.latch.Qn

	def setInput(self, Clk, Data):
		self.Clk = Clk
		self.Data = Data

	def getOutput(self):
		return (self.Q, self.Qn)

	def process(self):
		self.notGate.process()

		self.latch.Reset = self.notGate.Q
		self.latch.Set = self.notGate.A
		self.latch.process()

	def __repr__(self):
		states = [self.Clk, self.Data, self.Q, self.Qn]
		return self.buildTable(states)
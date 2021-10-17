from basicparts.Part import Part
from basicparts.Gates import And, Xor, Or

class HalfAdder(Part):
	def __init__(self):
		self.andGate = And()
		self.xorGate = Xor()

		super().__init__(numInputs=2, numOutputs=2,
						 name=HalfAdder.__name__,
						 lines=["A", "B", "Sum", "Carry"])

	@property
	def A(self):
		return self.andGate.A
	@A.setter
	def A(self, value):
		self.andGate.A = value
		self.xorGate.A = value

	@property
	def B(self):
		return self.andGate.B
	@B.setter
	def B(self, value):
		self.andGate.B = value
		self.xorGate.B = value

	@property
	def Sum(self):
		return self.xorGate.Q
	@property
	def Carry(self):
		return self.andGate.Q

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return (self.Sum, self.Carry)

	def process(self):
		self.andGate.process()
		self.xorGate.process()

	def __repr__(self):
		states = self.A, self.B, self.Sum, self.Carry
		return self.buildTable(states)

class FullAdder(Part):
	def __init__(self):
		self.orGate = Or()
		self.halfAdder1 = HalfAdder()
		self.halfAdder2 = HalfAdder()
		super().__init__(numInputs=3, numOutputs=2,
						 name=FullAdder.__name__,
						 lines=["Cin", "A", "B", "Sum", "Cout"])
	@property
	def A(self):
		return self.halfAdder1.A
	@A.setter
	def A(self, value):
		self.halfAdder1.A = value

	@property
	def B(self):
		return self.halfAdder1.B
	@B.setter
	def B(self, value):
		self.halfAdder1.B = value

	@property
	def Cin(self):
		return self.halfAdder2.B
	@Cin.setter
	def Cin(self, value):
		self.halfAdder2.B = value

	@property
	def Sum(self):
		return self.halfAdder2.Sum
	@property
	def Cout(self):
		return self.orGate.Q

	def setInput(self, Cin, A, B):
		self.A = A
		self.B = B
		self.Cin = Cin

	def getOutput(self):
		return (self.Sum, self.Cout)

	def process(self):
		self.halfAdder1.process()

		self.halfAdder2.A = self.halfAdder1.Sum
		self.halfAdder2.process()

		self.orGate.A = self.halfAdder2.Carry
		self.orGate.B = self.halfAdder1.Carry
		self.orGate.process()

	def __repr__(self):
		states = [self.Cin, self.A, self.B, self.Sum, self.Cout]
		return self.buildTable(states)

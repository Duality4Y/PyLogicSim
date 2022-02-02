from basicparts.Part import Part
from basicparts.Gates import And, Xor, Or

class HalfAdder(Part):
	def __init__(self):
		super().__init__(name=HalfAdder.__name__)
		
		self.andGate = And()
		self.xorGate = Xor()
		
		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Sum)
		self.addOutput(self.Carry)
	
	def A(self, *args):
		self.xorGate.A(*args)
		return self.andGate.A(*args)
	
	def B(self, *args):
		self.xorGate.B(*args)
		return self.andGate.B(*args)
	
	def Sum(self, *args):
		return self.xorGate.Q(*args)
	
	def Carry(self, *args):
		return self.andGate.Q(*args)

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return (self.Sum(), self.Carry())

	def process(self):
		self.andGate.process()
		self.xorGate.process()

class FullAdder(Part):
	def __init__(self):
		super().__init__(name=FullAdder.__name__)
		self.orGate = Or()
		self.halfAdder1 = HalfAdder()
		self.halfAdder2 = HalfAdder()
		
		self.addInput(self.Cin)
		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Sum)
		self.addOutput(self.Cout)

	def A(self, *args):
		return self.halfAdder1.A(*args)

	def B(self, *args):
		return self.halfAdder1.B(*args)

	def Cin(self, *args):
		return self.halfAdder2.B(*args)

	def Sum(self, *args):
		return self.halfAdder2.Sum(*args)
	
	def Cout(self, *args):
		return self.orGate.Q(*args)

	def setInput(self, Cin, A, B):
		self.A(A)
		self.B(B)
		self.Cin(Cin)

	def getOutput(self):
		return (self.Sum(), self.Cout())

	def process(self):
		self.halfAdder1.process()

		self.halfAdder2.A(self.halfAdder1.Sum())
		self.halfAdder2.process()

		self.orGate.A(self.halfAdder2.Carry())
		self.orGate.B(self.halfAdder1.Carry())
		self.orGate.process()

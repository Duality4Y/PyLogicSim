class Device(object):
	def __init__(self, numInputs=0, numOutputs=0):
		self.numInputs = numInputs
		self.numOutputs = numOutputs

class And(Device):
	def __init__(self):
		self.A = 0
		self.B = 0
		self.Q = 0

		super().__init__(numInputs=2, numOutputs=1)

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q = self.A & self.B

	def __repr__(self):
		return f"{self.A} | {self.B} | {self.Q}"

class Or(Device):
	def __init__(self):
		self.A = 0
		self.B = 0
		self.Q = 0

		super().__init__(numInputs=2, numOutputs=1)

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q = self.A | self.B

	def __repr__(self):
		return f"{self.A} | {self.B} | {self.Q}"

class Not(Device):
	def __init__(self):
		self.A = 0
		self.Q = 1

		super().__init__(numInputs=1, numOutputs=1)

	def setInput(self, A):
		self.A = A

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q =  0 if self.A else 1

	def __repr__(self):
		return f"{self.A} | {self.Q}"

class Nand(Device):
	def __init__(self):
		self.notGate = Not()
		self.andGate = And()

		super().__init__(numInputs=2, numOutputs=1)
	
	@property
	def A(self):
		return self.andGate.A
	@property
	def B(self):
		return self.andGate.B
	@property
	def Q(self):
		return self.notGate.Q

	def setInput(self, A, B):
		self.andGate.setInput(A, B)

	def getOutput(self):
		return self.notGate.getOutput()

	def process(self):
		self.andGate.process()

		self.notGate.setInput(self.andGate.getOutput())
		self.notGate.process()

	def __repr__(self):
		return f"{self.A} | {self.B} | {self.Q}"

class Nor(Device):
	def __init__(self):
		self.orGate = Or()
		self.notGate = Not()

		super().__init__(numInputs=2, numOutputs=1)
	
	@property
	def A(self):
		return self.orGate.A
	@property
	def B(self):
		return self.orGate.B
	@property
	def Q(self):
		return self.notGate.Q

	def setInput(self, A, B):
		self.orGate.setInput(A, B)

	def getOutput(self):
		return self.notGate.getOutput()

	def process(self):
		self.orGate.process()

		self.notGate.setInput(self.orGate.getOutput())
		self.notGate.process()

	def __repr__(self):
		return f"{self.A} | {self.B} | {self.Q}"

class Xor(Device):
	def __init__(self):
		self.nandGate 	= Nand()
		self.orGate 	= Or()
		self.andGate 	= And()

		super().__init__(numInputs=2, numOutputs=1)

	@property
	def A(self):
		return self.orGate.A
	@property
	def B(self):
		return self.orGate.B
	@property
	def Q(self):
		return self.andGate.Q

	def setInput(self, A, B):
		self.nandGate.setInput(A, B)
		self.orGate.setInput(A, B)

	def getOutput(self):
		return self.andGate.getOutput()

	def process(self):
		self.nandGate.process()
		self.orGate.process()

		self.andGate.setInput(self.nandGate.getOutput(), self.orGate.getOutput())
		self.andGate.process()

	def __repr__(self):
		return f"{self.A} | {self.B} | {self.Q}"

class Xnor(Device):
	def __init__(self):
		self.xorGate = Xor()
		self.notGate = Not()

		super().__init__(numInputs=2, numOutputs=1)

	def setInput(self, A, B):
		self.xorGate.setInput(A, B)

	def getOutput(self):
		return self.notGate.getOutput()

	def process(self):
		self.xorGate.process()

		self.notGate.setInput(self.xorGate.getOutput())
		self.notGate.process()

	def __repr__(self):
		return f"{self.xorGate.A} | {self.xorGate.B} | {self.notGate.Q}"
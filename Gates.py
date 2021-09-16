from Part import Part

class And(Part):
	def __init__(self):
		self.A = 0
		self.B = 0
		self.Q = 0

		super().__init__(numInputs=2, numOutputs=1,
						 name="And",
						 lines=["A", "B", "Q"])

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q = self.A & self.B

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)

class Or(Part):
	def __init__(self):
		self.A = 0
		self.B = 0
		self.Q = 0

		super().__init__(numInputs=2, numOutputs=1,
						 name="Or",
						 lines=["A", "B", "Q"])

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q = self.A | self.B

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)

class Not(Part):
	def __init__(self):
		self.A = 0
		self.Q = 1

		super().__init__(numInputs=1, numOutputs=1,
						 name="Not",
						 lines=["A", "Q"])

	def setInput(self, A):
		self.A = A

	def getOutput(self):
		return self.Q

	def process(self):
		self.Q =  0 if self.A else 1

	def __repr__(self):
		states = [self.A, self.Q]
		return self.buildTable(states)

class Nand(Part):
	def __init__(self):
		self.notGate = Not()
		self.andGate = And()

		super().__init__(numInputs=2, numOutputs=1,
						 name="Nand",
						 lines=["A", "B", "Q"])
	
	@property
	def A(self):
		return self.andGate.A
	@A.setter
	def A(self, value):
		self.andGate.A = value
	@property
	def B(self):
		return self.andGate.B
	@B.setter
	def B(self, value):
		self.andGate.B = value
	@property
	def Q(self):
		return self.notGate.Q

	def setInput(self, A, B):
		# self.andGate.setInput(A, B)
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.andGate.process()

		self.notGate.A = self.andGate.Q
		self.notGate.process()

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)

class Nor(Part):
	def __init__(self):
		self.orGate = Or()
		self.notGate = Not()

		super().__init__(numInputs=2, numOutputs=1,
						 name="Nor",
						 lines=["A", "B", "Q"])
	
	@property
	def A(self):
		return self.orGate.A
	@A.setter
	def A(self, value):
		self.orGate.A = value
	@property
	def B(self):
		return self.orGate.B
	@B.setter
	def B(self, value):
		self.orGate.B = value
	@property
	def Q(self):
		return self.notGate.Q

	def setInput(self, A, B):
		# self.orGate.setInput(A, B)
		self.A = A
		self.B = B
	def getOutput(self):
		return self.Q

	def process(self):
		self.orGate.process()

		self.notGate.A = self.orGate.Q
		self.notGate.process()

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)

class Xor(Part):
	def __init__(self):
		self.nandGate 	= Nand()
		self.orGate 	= Or()
		self.andGate 	= And()

		super().__init__(numInputs=2, numOutputs=1,
						 name="Xor",
						 lines=["A", "B", "Q"])

	@property
	def A(self):
		return self.orGate.A
	@A.setter
	def A(self, value):
		self.orGate.A = value
		self.nandGate.A = value
	@property
	def B(self):
		return self.orGate.B
	@B.setter
	def B(self, value):
		self.orGate.B = value
		self.nandGate.B = value

	@property
	def Q(self):
		return self.andGate.Q

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.nandGate.process()
		self.orGate.process()
		
		self.andGate.A = self.nandGate.Q
		self.andGate.B = self.orGate.Q
		self.andGate.process()

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)

class Xnor(Part):
	def __init__(self):
		self.xorGate = Xor()
		self.notGate = Not()

		super().__init__(numInputs=2, numOutputs=1,
						 name="Xnor",
						 lines=["A", "B", "Q"])
	@property
	def A(self):
		return self.xorGate.A
	@A.setter
	def A(self, value):
		self.xorGate.A = value

	@property
	def B(self):
		return self.xorGate.B
	@B.setter
	def B(self, value):
		self.xorGate.B = value

	@property
	def Q(self):
		return self.notGate.Q

	def setInput(self, A, B):
		self.A = A
		self.B = B

	def getOutput(self):
		return self.Q

	def process(self):
		self.xorGate.process()

		self.notGate.A = self.xorGate.Q
		self.notGate.process()

	def __repr__(self):
		states = [self.A, self.B, self.Q]
		return self.buildTable(states)
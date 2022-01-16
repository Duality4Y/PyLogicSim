from basicparts.Part import Part

class And(Part):
	def __init__(self):
		super().__init__(name="And")
		self._A = 0
		self._B = 0
		self._Q = 0

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)
	
	def A(self, *args):
		if args: self._A = args[0]
		return self._A
	
	def B(self, *args):
		if args: self._B = args[0]
		return self._B

	def Q(self, *args):
		if args:
			self._Q = args[0]
		return self._Q

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.Q(self.A() & self.B())

class Or(Part):
	def __init__(self):
		super().__init__(name="Or")
		self._A = 0
		self._B = 0
		self._Q = 0

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)
	
	def A(self, *args):
		if args: self._A = args[0]
		return self._A
	
	def B(self, *args):
		if args: self._B = args[0]
		return self._B

	def Q(self, *args):
		if args: self._Q = args[0]
		return self._Q

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.Q(self.A() | self.B())

class Not(Part):
	def __init__(self):
		super().__init__(name="Not")
		self._A = 0
		self._Q = 1

		self.addInput(self.A)
		self.addOutput(self.Q)
	
	def A(self, *args):
		if args: self._A = args[0]
		return self._A

	def Q(self, *args):
		if args: self._Q = args[0]
		return self._Q

	def setInput(self, A):
		self.A(A)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.Q(0 if self.A() else 1)

class Buffer(Part):
	def __init__(self):
		super().__init__(name="Buffer")
		self._A = 0
		self._Q = 0

		self.addInput(self.A)
		self.addOutput(self.Q)
	
	def A(self, *args):
		if args: self._A = args[0]
		return self._A

	def Q(self, *args):
		if args: self._Q = args[0]
		return self._Q

	def setInput(self, A):
		self.A(A)

	def process(self):
		self.Q(self.A())

class Nand(Part):
	def __init__(self):
		super().__init__(name="Nand")
		self.notGate = Not()
		self.andGate = And()

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)

	def A(self, *args):
		if args: self.andGate.A(*args)
		return self.andGate.A()
	
	def B(self, *args):
		if args: self.andGate.B(*args)
		return self.andGate.B()
	
	def Q(self, *args):
		if args: self.notGate.Q(*args)
		return self.notGate.Q()

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.andGate.process()

		self.notGate.A(self.andGate.Q())
		self.notGate.process()

class Nor(Part):
	def __init__(self):
		super().__init__(name="Nor")
		self.orGate = Or()
		self.notGate = Not()

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)

	def A(self, *args):
		if args: self.orGate.A(*args)
		return self.orGate.A()
	
	def B(self, *args):
		if args: self.orGate.B(*args)
		return self.orGate.B()
	
	def Q(self, *args):
		if args: self.notGate.Q(*args)
		return self.notGate.Q()

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.orGate.process()

		self.notGate.A(self.orGate.Q())
		self.notGate.process()

class Xor(Part):
	def __init__(self):
		super().__init__(name="Xor")
		self.nandGate 	= Nand()
		self.orGate 	= Or()
		self.andGate 	= And()

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)

	def A(self, *args):
		if args:
			self.orGate.A(*args)
			self.nandGate.A(*args)
		return self.orGate.A()
	
	def B(self, *args):
		if args:
			self.orGate.B(*args)
			self.nandGate.B(*args)
		return self.orGate.B()
	
	def Q(self, *args):
		if args: self.andGate.Q(*args)
		return self.andGate.Q()

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.nandGate.process()
		self.orGate.process()
		
		self.andGate.A(self.nandGate.Q())
		self.andGate.B(self.orGate.Q())
		self.andGate.process()

class Xnor(Part):
	def __init__(self):
		super().__init__(name="Xnor")
		self.xorGate = Xor()
		self.notGate = Not()

		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q)

	def A(self, *args):
		if args:
			self.xorGate.A(*args)
		return self.xorGate.A()
	
	def B(self, *args):
		if args:
			self.xorGate.B(*args)
		return self.xorGate.B()
	
	def Q(self, *args):
		if args: self.notGate.Q(*args)
		return self.notGate.Q()

	def setInput(self, A, B):
		self.A(A)
		self.B(B)

	def getOutput(self):
		return self.Q()

	def process(self):
		self.xorGate.process()

		self.notGate.A(self.xorGate.Q())
		self.notGate.process()
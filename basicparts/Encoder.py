from basicparts.Part import Part
from basicparts.Gates import Not, And, Or

class Decoder(Part):
	def __init__(self):
		super().__init__(name=Decoder.__name__)

		self.not1 = Not()
		self.not2 = Not()
		self.and1 = And()
		self.and2 = And()
		self.and3 = And()
		self.and4 = And()
		
		# enable gates
		self.and5 = And()
		self.and6 = And()
		self.and7 = And()
		self.and8 = And()
	
		self.addInput(self.Enable)
		self.addInput(self.A)
		self.addInput(self.B)
		self.addOutput(self.Q1)
		self.addOutput(self.Q2)
		self.addOutput(self.Q3)
		self.addOutput(self.Q4)
	
	def A(self, *args):
		return self.not1.A(*args)

	def B(self, *args):
		return self.not2.A(*args)
	
	def Enable(self, *args):
		self.and5.B(*args)
		self.and6.B(*args)
		self.and7.B(*args)
		return self.and8.B(*args)
	
	def Q1(self, *args):
		return self.and5.Q(*args)
	def Q2(self, *args):
		return self.and6.Q(*args)
	def Q3(self, *args):
		return self.and7.Q(*args)
	def Q4(self, *args):
		return self.and8.Q(*args)

	def setInput(self, Enable, A, B):
		self.A(A)
		self.B(B)
		self.Enable(Enable) 

	def process(self):
		self.not1.process()
		self.not2.process()
		Ac = self.not1.Q()
		Bc = self.not2.Q()

		self.and1.setInput(Ac,		 Bc)
		self.and2.setInput(Ac, 		 self.B())
		self.and3.setInput(self.A(), Bc)
		self.and4.setInput(self.A(), self.B())

		self.and1.process()
		self.and2.process()
		self.and3.process()
		self.and4.process()

		self.and5.A(self.and1.Q())
		self.and6.A(self.and2.Q())
		self.and7.A(self.and3.Q())
		self.and8.A(self.and4.Q())

		self.and5.process()
		self.and6.process()
		self.and7.process()
		self.and8.process()

class Encoder(Part):
	pass
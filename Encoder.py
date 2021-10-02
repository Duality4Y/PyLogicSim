from Part import Part
from Gates import Not, And, Or

class Decoder(Part):
	def __init__(self):
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


		super().__init__(numInputs=3, numOutputs=4,
						 name="Decoder",
						 lines=["Enable", "A", "B", "Q1", "Q2", "Q3", "Q4"])
	@property
	def A(self):
		return self.not1.A
	@A.setter
	def A(self, value):
		self.not1.A = value

	@property
	def B(self):
		return self.not2.A
	@B.setter
	def B(self, value):
		self.not2.A = value

	@property
	def Enable(self):
		return self.and5.B
	@Enable.setter
	def Enable(self, value):
		self.and5.B = value
		self.and6.B = value
		self.and7.B = value
		self.and8.B = value

	@property
	def Q1(self):
		return self.and5.Q
	@property
	def Q2(self):
		return self.and6.Q
	@property
	def Q3(self):
		return self.and7.Q
	@property
	def Q4(self):
		return self.and8.Q

	def setInput(self, Enable, A, B):
		self.A = A
		self.B = B
		self.Enable = Enable 

	def process(self):
		self.not1.process()
		self.not2.process()
		Ac = self.not1.Q
		Bc = self.not2.Q

		self.and1.setInput(Ac, Bc)
		self.and2.setInput(Ac, self.B)
		self.and3.setInput(self.A, Bc)
		self.and4.setInput(self.A, self.B)

		self.and1.process()
		self.and2.process()
		self.and3.process()
		self.and4.process()

		self.and5.A = self.and1.Q
		self.and6.A = self.and2.Q
		self.and7.A = self.and3.Q
		self.and8.A = self.and4.Q

		self.and5.process()
		self.and6.process()
		self.and7.process()
		self.and8.process()

	def __repr__(self):
		states = [self.Enable, self.A, self.B, self.Q1, self.Q2, self.Q3, self.Q4]
		return self.buildTable(states)


class Encoder(Part):
	pass
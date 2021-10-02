from Part import Part
from Gates import And, Or
from Encoder import Decoder

class Mux(Part):
	def __init__(self):
		self.decoder = Decoder()
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.andGate4 = And()

		self.andGate5 = And() # enable gate for the output
		
		self.orGate1 = Or()
		self.orGate2 = Or()
		self.orGate3 = Or()

		super().__init__(numInputs=7, numOutputs=1,
						 name="Multiplexer",
						 lines=["Enable", "S0", "S1", "I0", "I1", "I2", "I3", "Q"])
	@property
	def Enable(self):
		return self.decoder.Enable
	@Enable.setter
	def Enable(self, value):
		self.decoder.Enable = value
		self.andGate5.A = value

	@property
	def S0(self):
		return self.decoder.A
	@S0.setter
	def S0(self, value):
		self.decoder.A = value
	@property
	def S1(self):
		return self.decoder.B
	@S1.setter
	def S1(self, value):
		self.decoder.B = value

	@property
	def I0(self):
		return self.andGate1.A
	@I0.setter
	def I0(self, value):
		self.andGate1.A = value
	@property
	def I1(self):
		return self.andGate2.A
	@I1.setter
	def I1(self, value):
		self.andGate2.A = value
	@property
	def I2(self):
		return self.andGate3.A
	@I2.setter
	def I2(self, value):
		self.andGate3.A = value
	@property
	def I3(self):
		return self.andGate4.A
	@I3.setter
	def I3(self, value):
		self.andGate4.A = value

	@property
	def Q(self):
		return self.orGate3.Q

	def setInput(self, Enable, S0, S1, I0, I1, I2, I3):
		self.Enable = Enable
		self.S0 = S0
		self.S1 = S1
		self.I0 = I0
		self.I1 = I1
		self.I2 = I2
		self.I3 = I3

	def process(self):
		self.decoder.process()

		self.andGate1.B = self.decoder.Q1
		self.andGate2.B = self.decoder.Q2
		self.andGate3.B = self.decoder.Q3
		self.andGate4.B = self.decoder.Q4

		self.andGate1.process()
		self.andGate2.process()
		self.andGate3.process()
		self.andGate4.process()

		self.orGate1.A = self.andGate1.Q
		self.orGate1.B = self.andGate2.Q
		self.orGate2.A = self.andGate3.Q
		self.orGate2.B = self.andGate4.Q
		self.orGate1.process()
		self.orGate2.process()

		self.orGate3.A = self.orGate1.Q
		self.orGate3.B = self.orGate2.Q
		self.orGate3.process()

		self.andGate5.B = self.orGate3.B
		self.andGate5.process()

	def __repr__(self):
		states = [self.Enable, self.S0, self.S1, self.I0, self.I1, self.I2, self.I3, self.Q]
		return self.buildTable(states)

class DeMux(Part):
	def __init__(self):
		# selects which and gate lets a signal through
		self.decoder = Decoder()

		# and gates that let selected signal through
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.andGate4 = And()

		# and gates for enable
		self.andGate5 = And()
		self.andGate6 = And()
		self.andGate7 = And()
		self.andGate8 = And()

		super().__init__(numInputs=4, numOutputs=4,
						 name="Demultiplexer",
						 lines=["Enable", "Input", "S0", "S1", "Q0", "Q1", "Q2", "Q3"])
	@property
	def Enable(self):
		return self.andGate5.B
	@Enable.setter
	def Enable(self, value):
		self.decoder.Enable = value
		self.andGate5.B = value
		self.andGate6.B = value
		self.andGate7.B = value
		self.andGate8.B = value
	@property
	def Input(self):
		return self.andGate1.A
	@Input.setter
	def Input(self, value):
		self.andGate1.A = value
		self.andGate2.A = value
		self.andGate3.A = value
		self.andGate4.A = value

	@property
	def S0(self):
		return self.decoder.A
	@S0.setter
	def S0(self, value):
		self.decoder.A = value
	@property
	def S1(self):
		return self.decoder.B
	@S1.setter
	def S1(self, value):
		self.decoder.B = value

	@property
	def Q0(self):
		return self.andGate5.Q
	@property
	def Q1(self):
		return self.andGate6.Q
	@property
	def Q2(self):
		return self.andGate7.Q
	@property
	def Q3(self):
		return self.andGate8.Q

	def setInput(self, Enable, Input, S0, S1):
		self.Enable = Enable
		self.Input = Input
		self.S0 = S0
		self.S1 = S1

	def process(self):
		self.decoder.process()
		self.andGate1.B = self.decoder.Q1
		self.andGate2.B = self.decoder.Q2
		self.andGate3.B = self.decoder.Q3
		self.andGate4.B = self.decoder.Q4
		self.andGate1.process()
		self.andGate2.process()
		self.andGate3.process()
		self.andGate4.process()

		self.andGate5.A = self.andGate1.Q
		self.andGate6.A = self.andGate2.Q
		self.andGate7.A = self.andGate3.Q
		self.andGate8.A = self.andGate4.Q
		self.andGate5.process()
		self.andGate6.process()
		self.andGate7.process()
		self.andGate8.process()


	def __repr__(self):
		states = [self.Enable, self.Input, self.S0, self.S1, self.Q0, self.Q1, self.Q2, self.Q3]
		return self.buildTable(states)

def TestMux(part):
	print("Testing '{0}' part.".format(part.name))
	print(part.getLineTable())
	for inputBit in range(0, 2 ** 2):
		for i in range(0, 2 ** 2):
			inValues = [0] * 4
			inValues[inputBit] = 1
			for bitPos in range(0, 2):
				inValues.insert(0, (i >> bitPos) & 0x01)
			inValues.insert(0, 1) # always enable?
			# print(*inValues)
			part.setInput(*inValues)
			part.process()
			print(part)
	print()
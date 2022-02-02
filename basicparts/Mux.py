from basicparts.Part import Part
from basicparts.Gates import And, Or
from basicparts.Encoder import Decoder

class Mux(Part):
	def __init__(self):
		super().__init__(name=Mux.__name__)

		self.decoder = Decoder()
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.andGate4 = And()

		self.andGate5 = And() # enable gate for the output
		
		self.orGate1 = Or()
		self.orGate2 = Or()
		self.orGate3 = Or()

		self.addInput(self.Enable)
		self.addInput(self.S0)
		self.addInput(self.S1)
		self.addInput(self.I0)
		self.addInput(self.I1)
		self.addInput(self.I2)
		self.addInput(self.I3)
		self.addOutput(self.Q)
	
	def Enable(self, *args):
		self.decoder.Enable(*args)
		return self.andGate5.A(*args)
	
	def S0(self, *args):
		return self.decoder.A(*args)
	
	def S1(self, *args):
		return self.decoder.B(*args)
	
	def I0(self, *args):
		return self.andGate1.A(*args)
	
	def I1(self, *args):
		return self.andGate2.A(*args)
	
	def I2(self, *args):
		return self.andGate3.A(*args)
	
	def I3(self, *args):
		return self.andGate4.A(*args)
	
	def Q(self, *args):
		return self.orGate3.Q(*args)

	def setInput(self, Enable, S0, S1, I0, I1, I2, I3):
		self.Enable(Enable)
		self.S0(S0)
		self.S1(S1)
		self.I0(I0)
		self.I1(I1)
		self.I2(I2)
		self.I3(I3)

	def process(self):
		self.decoder.process()

		self.andGate1.B(self.decoder.Q1())
		self.andGate2.B(self.decoder.Q2())
		self.andGate3.B(self.decoder.Q3())
		self.andGate4.B(self.decoder.Q4())

		self.andGate1.process()
		self.andGate2.process()
		self.andGate3.process()
		self.andGate4.process()

		self.orGate1.A(self.andGate1.Q())
		self.orGate1.B(self.andGate2.Q())
		self.orGate2.A(self.andGate3.Q())
		self.orGate2.B(self.andGate4.Q())
		self.orGate1.process()
		self.orGate2.process()

		self.orGate3.A(self.orGate1.Q())
		self.orGate3.B(self.orGate2.Q())
		self.orGate3.process()

		self.andGate5.B(self.orGate3.B())
		self.andGate5.process()

class DeMux(Part):
	def __init__(self):
		super().__init__(name=DeMux.__name__)

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

		
		self.addInput(self.Enable)
		self.addInput(self.Input)
		self.addInput(self.S0)
		self.addInput(self.S1)

		self.addOutput(self.Q0)
		self.addOutput(self.Q1)
		self.addOutput(self.Q2)
		self.addOutput(self.Q3)
	
	def Enable(self, *args):
		self.decoder.Enable(*args)
		self.andGate5.B(*args)
		self.andGate6.B(*args)
		self.andGate7.B(*args)
		return self.andGate8.B(*args)

	def Input(self, *args):
		self.andGate1.A(*args)
		self.andGate2.A(*args)
		self.andGate3.A(*args)
		return self.andGate4.A(*args)

	def S0(self, *args):
		return self.decoder.A(*args)
	
	def S1(self, *args):
		return self.decoder.B(*args)

	def Q0(self, *args):
		return self.andGate5.Q(*args)

	def Q1(self, *args):
		return self.andGate6.Q(*args)

	def Q2(self, *args):
		return self.andGate7.Q(*args)

	def Q3(self, *args):
		return self.andGate8.Q(*args)

	def setInput(self, Enable, Input, S0, S1):
		self.Enable(Enable)
		self.Input(Input)
		self.S0(S0)
		self.S1(S1)

	def process(self):
		self.decoder.process()
		self.andGate1.B(self.decoder.Q1())
		self.andGate2.B(self.decoder.Q2())
		self.andGate3.B(self.decoder.Q3())
		self.andGate4.B(self.decoder.Q4())
		self.andGate1.process()
		self.andGate2.process()
		self.andGate3.process()
		self.andGate4.process()

		self.andGate5.A(self.andGate1.Q())
		self.andGate6.A(self.andGate2.Q())
		self.andGate7.A(self.andGate3.Q())
		self.andGate8.A(self.andGate4.Q())
		self.andGate5.process()
		self.andGate6.process()
		self.andGate7.process()
		self.andGate8.process()

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
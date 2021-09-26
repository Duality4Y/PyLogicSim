from Part import Part
from Gates import And, Or, Not, Nand, Nor, Xor, Xnor
from Latch import SRLatch, GatedLatch, DataLatch
from FlipFlop import FlipFlop, DFlipFlop, TFlipFlop
from Adder import HalfAdder, FullAdder

from TestUtils import TestPart, TestFlipFlop

class LogicUnit(Part):
	def __init__(self):
		self.notData = Not()
		self.notResult = Not()

		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.orGate1 = Or()
		self.orGate2 = Or()
		self.orGate3 = Or()

		self.andGate4 = And()
		self.andGate5 = And()
		self.andGate6 = And()
		self.orGate4 = Or()
		self.orGate5 = Or()

		super().__init__(numInputs=9, numOutputs=1,
				 name="LogicUnit",
				 lines=["RIn",
				 		"Data",
				 		"ROut",
				 		"LD/OR", "LDC/ORC", "AND/XNOR", "ANDC", "OR/ORC", "XNOR"])
	@property
	def Data(self):
		return self.andGate6.B
	@Data.setter
	def Data(self, value):
		self.andGate6.B = value
	
	@property
	def RIn(self):
		return self.andGate1.B
	@RIn.setter
	def RIn(self, value):
		self.andGate1.B = value
		self.andGate3.B = value
		self.andGate5.B = value
	
	@property
	def ROut(self):
		return self.orGate4.Q
	
	@property
	def LD_OR(self):
		return self.orGate3.A
	@LD_OR.setter
	def LD_OR(self, value):
		self.orGate3.A = value
	
	@property
	def LDC_ORC(self):
		return self.orGate1.A
	@LDC_ORC.setter
	def LDC_ORC(self, value):
		self.orGate1.A = value
	
	@property
	def AND_XNOR(self):
		return self.andGate3.A
	@AND_XNOR.setter
	def AND_XNOR(self, value):
		self.andGate3.A = value
	
	@property
	def ANDC(self):
		return self.andGate1.A
	@ANDC.setter
	def ANDC(self, value):
		self.andGate1.A = value
	
	@property
	def OR_ORC(self):
		return self.andGate5.A
	@OR_ORC.setter
	def OR_ORC(self, value):
		self.andGate5.A = value
	
	@property
	def XNOR(self):
		return self.andGate2.A
	@XNOR.setter
	def XNOR(self, value):
		self.andGate2.A = value

	def setInput(self, RIn, Data, LD_OR, LDC_ORC, AND_XNOR, ANDC, OR_ORC, XNOR):
		self.Data = Data
		self.RIn = RIn
		self.LD_OR = LD_OR
		self.LDC_ORC = LDC_ORC
		self.AND_XNOR = AND_XNOR
		self.ANDC = ANDC
		self.OR_ORC = OR_ORC
		self.XNOR = XNOR

	def getOutput(self):
		return self.ROut

	def process(self):
		self.notData.A = self.Data
		self.notData.process()
		self.notResult.A = self.RIn
		self.notResult.process()

		self.andGate1.process()

		self.andGate2.B = self.notResult.Q
		self.andGate2.process()

		self.andGate3.process()

		self.orGate2.A = self.andGate1.Q
		self.orGate2.B = self.andGate2.Q
		self.orGate2.process()

		self.orGate3.B = self.andGate3.Q
		self.orGate3.process()

		self.orGate1.B = self.orGate2.Q
		self.orGate1.process()

		self.andGate4.A = self.orGate1.Q
		self.andGate4.B = self.notData.Q
		self.andGate4.process()

		self.andGate5.process()

		self.andGate6.A = self.orGate3.Q
		self.andGate6.process()

		self.orGate5.A = self.andGate5.Q
		self.orGate5.B = self.andGate6.Q
		self.orGate5.process()

		self.orGate4.A = self.andGate4.Q 
		self.orGate4.B = self.orGate5.Q
		self.orGate4.process()

	def __repr__(self):
		states = [self.RIn, self.Data, self.ROut,
				  self.LD_OR, self.LDC_ORC, self.AND_XNOR, self.ANDC, self.OR_ORC, self.XNOR]
		return self.buildTable(states)

def TestLU():
	inputTable = [("LD", [1, 0, 0, 0, 0, 0]), # LD
				  ("OR", [1, 0, 0, 0, 1, 0]), # OR
				  ("LDC", [0, 1, 0, 0, 0, 0]), # LDC
				  ("ORC", [0, 1, 0, 0, 1, 0]), # ORC
				  ("AND", [0, 0, 1, 0, 0, 0]), # AND
				  ("XNOR", [0, 0, 1, 0, 0, 1]), # XNOR
				  ("ANDC", [0, 0, 0, 1, 0, 0]), # ANDC
				  ]

	logicUnit = LogicUnit()
	print("Testing '{0}' part.".format(logicUnit.name))

	for name, inputSet in inputTable:
		print("Testing '{0}' functionality".format(name))
		print(logicUnit.getLineTable())
		for i in range(0, 4):
			Data = (i & 0x01)
			RIn = (i >> 1) & 0x01
			# print([Data, RIn] + inputSet)
			inputs = [RIn, Data] + inputSet
			logicUnit.setInput(*inputs)
			logicUnit.process()
			print(logicUnit)
		print()

if __name__ == "__main__":
	print("Hello, world!")

	TestPart(And())
	TestPart(Or())
	TestPart(Not())
	TestPart(Nand())
	TestPart(Nor())
	TestPart(Xor())
	TestPart(Xnor())

	TestPart(SRLatch())
	TestPart(GatedLatch())
	TestPart(DataLatch())

	TestPart(HalfAdder())
	TestPart(FullAdder())

	TestFlipFlop(FlipFlop())
	TestFlipFlop(DFlipFlop())
	TestFlipFlop(TFlipFlop())

	TestLU()

	# logicUnit.RIn, logicUnit.Data = 0, 0
	# logicUnit.XNOR, logicUnit.AND_XNOR = 1, 1

	# logicUnit.process()
	# print(logicUnit)

	# logicUnit.RIn, logicUnit.Data = 0, 1
	# logicUnit.XNOR, logicUnit.AND_XNOR = 1, 1
	# logicUnit.process()
	# print(logicUnit)

	# logicUnit.RIn, logicUnit.Data = 1, 0
	# logicUnit.XNOR, logicUnit.AND_XNOR = 1, 1
	# logicUnit.process()
	# print(logicUnit)

	# logicUnit.RIn, logicUnit.Data = 1, 1
	# logicUnit.XNOR, logicUnit.AND_XNOR = 1, 1
	# logicUnit.process()
	# print(logicUnit)
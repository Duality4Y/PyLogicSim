from basicparts.Part import Part
from basicparts.Gates import Not, And, Or, Nor, Buffer
from basicparts.FlipFlop import DFlipFlop
from basicparts.Latch import DataLatch, GatedLatch

class Instructions(object):
	def __init__(self):
		(self.NOPO,
		 self.LD,
		 self.LDC,
		 self.AND,
		 self.ANDC,
		 self.OR,
		 self.ORC,
		 self.XNOR,
		 self.STO,
		 self.STOC,
		 self.IEN,
		 self.OEN,
		 self.JMP,
		 self.RTN,
		 self.SKZ,
		 self.NOPF) = [i for i in range(0, 0x10)]

class LogicUnit(Part):
	def __init__(self):
		super().__init__(name=LogicUnit.__name__)
		
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

	
		self.addInput(self.RIn)
		self.addInput(self.Data)
		self.addInput(self.LD_OR)
		self.addInput(self.LDC_ORC)
		self.addInput(self.AND_XNOR)
		self.addInput(self.ANDC)
		self.addInput(self.OR_ORC)
		self.addInput(self.XNOR)
		self.addOutput(self.ROut)
	
	def Data(self, *args):
		return self.andGate6.B(*args)
	
	def RIn(self, *args):
		self.andGate1.B(*args)
		self.andGate3.B(*args)
		return self.andGate5.B(*args)
	
	def ROut(self, *args):
		return self.orGate4.Q(*args)
	
	def LD_OR(self, *args):
		return self.orGate3.A(*args)
	
	def LDC_ORC(self, *args):
		return self.orGate1.A(*args)

	def AND_XNOR(self, *args):
		return self.andGate3.A(*args)
	
	def ANDC(self, *args):
		return self.andGate1.A(*args)
	
	def OR_ORC(self, *args):
		return self.andGate5.A(*args)
	
	def XNOR(self, *args):
		return self.andGate2.A(*args)

	def setInput(self, RIn, Data, LD_OR, LDC_ORC, AND_XNOR, ANDC, OR_ORC, XNOR):
		self.Data(Data)
		self.RIn(RIn)
		self.LD_OR(LD_OR)
		self.LDC_ORC(LDC_ORC)
		self.AND_XNOR(AND_XNOR)
		self.ANDC(ANDC)
		self.OR_ORC(OR_ORC)
		self.XNOR(XNOR)

	def getOutput(self):
		return (self.ROut())

	def process(self):
		self.notData.A(self.Data())
		self.notData.process()
		self.notResult.A(self.RIn())
		self.notResult.process()

		self.andGate1.process()

		self.andGate2.B(self.notResult.Q())
		self.andGate2.process()

		self.andGate3.process()

		self.orGate2.A(self.andGate1.Q())
		self.orGate2.B(self.andGate2.Q())
		self.orGate2.process()

		self.orGate3.B(self.andGate3.Q())
		self.orGate3.process()

		self.orGate1.B(self.orGate2.Q())
		self.orGate1.process()

		self.andGate4.A(self.orGate1.Q())
		self.andGate4.B(self.notData.Q())
		self.andGate4.process()

		self.andGate5.process()

		self.andGate6.A(self.orGate3.Q())
		self.andGate6.process()

		self.orGate5.A(self.andGate5.Q())
		self.orGate5.B(self.andGate6.Q())
		self.orGate5.process()

		self.orGate4.A(self.andGate4.Q())
		self.orGate4.B(self.orGate5.Q())
		self.orGate4.process()

class Decoder(Part):
	def __init__(self, lineEncoder3=Buffer(), lineEncoder2=Buffer(), lineEncoder1=Buffer(), lineEncoder0=Buffer()):
		super().__init__(name=Decoder.__name__)
		""" 
			Arguments determine what value to decode.
			Value consists of Buffers() and Not() Gates Not() represents a bit
			and a Buffer() represents the complement of the bit in this specific Decoder.
			so a value of 8 (1000) is: buffer(), Not(), Not(), Not() for arguments.
		"""
		self.lineEncoder0 = lineEncoder0
		self.lineEncoder1 = lineEncoder1
		self.lineEncoder2 = lineEncoder2
		self.lineEncoder3 = lineEncoder3

		self.norGate1 = Nor()
		self.norGate2 = Nor()
		self.andGate = And()

		self.addInput(self.I3)
		self.addInput(self.I2)
		self.addInput(self.I1)
		self.addInput(self.I0)
		self.addOutput(self.Q)
	
	def I3(self, *args):
		return self.lineEncoder3.A(*args)
	
	def I2(self, *args):
		return self.lineEncoder2.A(*args)
	
	def I1(self, *args):
		return self.lineEncoder1.A(*args)
	
	def I0(self, *args):
		return self.lineEncoder0.A(*args)
	
	def Q(self, *args):
		return self.andGate.Q(*args)

	def setInput(self, I3, I2, I1, I0):
		self.I3(I3)
		self.I2(I2)
		self.I1(I1)
		self.I0(I0)

	def process(self):
		self.lineEncoder0.process()
		self.lineEncoder1.process()
		self.lineEncoder2.process()
		self.lineEncoder3.process()

		self.norGate1.A(self.lineEncoder0.Q())
		self.norGate1.B(self.lineEncoder1.Q())
		self.norGate2.A(self.lineEncoder2.Q())
		self.norGate2.B(self.lineEncoder3.Q())
		self.norGate1.process()
		self.norGate2.process()

		self.andGate.A(self.norGate1.Q())
		self.andGate.B(self.norGate2.Q())
		self.andGate.process()

class InstrDecoder(Part):
	def __init__(self):
		super().__init__(name=InstrDecoder.__name__)
		
		""" To lazy to code 16 decoders so generating a set of decoders instead. """
		self.decoders = []
		for i in range(0, 16):
			S3 = (i >> 3) & 0x01
			S2 = (i >> 2) & 0x01
			S1 = (i >> 1) & 0x01
			S0 = i & 0x01
			selectLines = [Not() if select else Buffer() for select in [S3, S2, S1, S0]]
			decoder = Decoder(*selectLines)
			self.decoders.append(decoder)

		self.addInput(self.I3)
		self.addInput(self.I2)
		self.addInput(self.I1)
		self.addInput(self.I0)

		self.addOutput(self.NOPO)
		self.addOutput(self.LD)
		self.addOutput(self.LDC)
		self.addOutput(self.AND)

		self.addOutput(self.ANDC)
		self.addOutput(self.OR)
		self.addOutput(self.ORC)
		self.addOutput(self.XNOR)
		
		self.addOutput(self.STO)
		self.addOutput(self.STOC)
		self.addOutput(self.IEN)
		self.addOutput(self.OEN)
		
		self.addOutput(self.JMP)
		self.addOutput(self.RTN)
		self.addOutput(self.SKZ)
		self.addOutput(self.NOPF)
	
	def I3(self, *args):
		for decoder in self.decoders:
			decoder.I3(*args)
		return self.decoders[0].I3(*args)
	
	def I2(self, *args):
		for decoder in self.decoders:
			decoder.I2(*args)
		return self.decoders[0].I2(*args)
	
	def I1(self, *args):
		for decoder in self.decoders:
			decoder.I1(*args)
		return self.decoders[0].I1(*args)
	
	def I0(self, *args):
		for decoder in self.decoders:
			decoder.I0(*args)
		return self.decoders[0].I0(*args)


	def NOPO(self, *args):
		return self.decoders[0].Q(*args)

	def LD(self, *args):
		return self.decoders[1].Q(*args)

	def LDC(self, *args):
		return self.decoders[2].Q(*args)

	def AND(self, *args):
		return self.decoders[3].Q(*args)

	def ANDC(self, *args):
		return self.decoders[4].Q(*args)

	def OR(self, *args):
		return self.decoders[5].Q(*args)

	def ORC(self, *args):
		return self.decoders[6].Q(*args)

	def XNOR(self, *args):
		return self.decoders[7].Q(*args)

	def STO(self, *args):
		return self.decoders[8].Q(*args)

	def STOC(self, *args):
		return self.decoders[9].Q(*args)

	def IEN(self, *args):
		return self.decoders[10].Q(*args)

	def OEN(self, *args):
		return self.decoders[11].Q(*args)

	def JMP(self, *args):
		return self.decoders[12].Q(*args)

	def RTN(self, *args):
		return self.decoders[13].Q(*args)

	def SKZ(self, *args):
		return self.decoders[14].Q(*args)

	def NOPF(self, *args):
		return self.decoders[15].Q(*args)

	def setInput(self, *args):
		for decoder in self.decoders:
			decoder.setInput(*args)

	def process(self):
		for decoder in self.decoders:
			decoder.process()

class Mux(Part):
	def __init__(self):
		super().__init__(name=Mux.__name__)
		
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.andGate4 = And()
		self.notGate1 = Not()
		self.notGate2 = Not()
		self.orGate1 = Or()

		self.addInput(self.A)
		self.addInput(self.B)
		self.addInput(self.S0)
		self.addInput(self.S1)
		self.addOutput(self.Q)
	
	def A(self, *args):
		return self.andGate1.A(*args)
	
	def B(self, *args):
		return self.andGate2.B(*args)
	
	def S0(self, *args):
		return self.andGate1.B(*args)
	
	def S1(self, *args):
		return self.andGate4.A(*args)
	
	def Q(self, *args):
		return self.orGate1.Q(*args)

	def setInput(self, A, B, S0, S1):
		self.A(A)
		self.B(B)
		self.S0(S0)
		self.S1(S1)

	def process(self):
		self.notGate1.A(self.S1())
		self.notGate2.A(self.S0())
		self.notGate1.process()
		self.notGate2.process()

		self.andGate1.process()
		self.andGate2.A(self.notGate2.Q())
		self.andGate2.process()

		self.andGate3.A(self.andGate1.Q())
		self.andGate3.B(self.notGate1.Q())
		self.andGate3.process()

		self.andGate4.B(self.andGate2.Q())
		self.andGate4.process()

		self.orGate1.A(self.andGate3.Q())
		self.orGate1.B(self.andGate4.Q())
		self.orGate1.process()

class InstrRegister(Part):
	def __init__(self):
		super().__init__(name="Instruction Register")
		
		self.registers = [DFlipFlop() for i in range(4)]

		self.notgate = Not()

		self.addInput(self.Clk)
		self.addInput(self.I3)
		self.addInput(self.I2)
		self.addInput(self.I1)
		self.addInput(self.I0)
		self.addOutput(self.Q3)
		self.addOutput(self.Q2)
		self.addOutput(self.Q1)
		self.addOutput(self.Q0)

	def Clk(self, *args):
		# for reg in self.registers:
		# 	reg.Clk(*args)
		# return self.registers[0].Clk(*args)
		return self.notgate.A(*args)
	
	def I0(self, *args):
		return self.registers[0].Data(*args)
	
	def I1(self, *args):
		return self.registers[1].Data(*args)
	
	def I2(self, *args):
		return self.registers[2].Data(*args)
	
	def I3(self, *args):
		return self.registers[3].Data(*args)
	
	def Q0(self, *args):
		return self.registers[0].Q(*args)
	
	def Q1(self, *args):
		return self.registers[1].Q(*args)
	
	def Q2(self, *args):
		return self.registers[2].Q(*args)
	
	def Q3(self, *args):
		return self.registers[3].Q(*args)

	def setInput(self, Clk, I3, I2, I1, I0):
		self.Clk(Clk)
		self.I0(I0)
		self.I1(I1)
		self.I2(I2)
		self.I3(I3)

	def process(self):
		self.notgate.process()
		for register in self.registers:
			register.Clk(self.notgate.Q())
			register.process()

class DInRegister(Part):
	def __init__(self):
		super().__init__(name=DInRegister.__name__)

		self.reg = DFlipFlop()
		self.andGate = And()
		self.notGate = Not()
		
		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Qr)
		self.addOutput(self.Q)
	
	def Clk(self, *args):
		return self.notGate.A(*args)
	
	def Data(self, *args):
		return self.reg.Data(*args)

	def Q(self, *args):
		return self.andGate.Q(*args)
	
	def Qr(self, *args):
		return self.reg.Q(*args)
	
	def setInput(self, Clk, Data):
		self.Clk(Clk)
		self.Data(Data)
	
	def process(self):
		self.notGate.process()

		self.reg.Clk(self.notGate.Q())
		self.reg.process()
		
		self.andGate.A(self.Data())
		self.andGate.B(self.reg.Q())
		self.andGate.process()

class DOutRegister(Part):
	def __init__(self):
		super().__init__(name=DOutRegister.__name__)

		self.reg = DFlipFlop()
		self.notGate = Not()
		
		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Q)
	
	def Clk(self, *args):
		return self.notGate.A(*args)
	
	def Data(self, *args):
		return self.reg.Data(*args)
	
	def Q(self, *args):
		return self.reg.Q(*args)
	
	def setInput(self, Clk, Data):
		self.Clk(Clk)
		self.Data(Data)
	
	def process(self):
		self.notGate.process()

		self.reg.Clk(self.notGate.Q())
		self.reg.process()

class FlagRegister(Part):
	def __init__(self):
		super().__init__(name=FlagRegister.__name__)
		
		self.reg = DataLatch()
		
		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Q)
	
	def Clk(self, *args):
		return self.reg.Clk(*args)

	def Data(self, *args):
		return self.reg.Data(*args)
	
	def Q(self, *args):
		return self.reg.Q(*args)
	
	def setInput(self, Data, Clk):
		self.Data(Data)
		self.Clk(Clk)
	
	def process(self):
		self.reg.process()

class ResultRegister(Part):
	def __init__(self):
		super().__init__(name=ResultRegister.__name__)

		self.reg = DFlipFlop()
		self.andGate = And()

		self.addInput(self.Clk)
		self.addInput(self.Data)
		self.addOutput(self.Q)
		self.addOutput(self.Qn)

		self.reg.Data(0)
		self.Clk(1)
		self.process()
		self.Clk(0)
		self.process()

	def Data(self, *args):
		return self.reg.Data(*args)
	
	def Clk(self, *args):
		return self.reg.Clk(*args)
	
	def Q(self, *args):
		return self.reg.Q(*args)
	
	def Qn(self, *args):
		return self.reg.Qn(*args)
	
	def setInput(self, Data, Clk):
		self.Data(Data)
		self.Clk(Clk)

	def process(self):
		self.reg.Clk()
		self.reg.process()

class ControlUnit(Part):
	def __init__(self):
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.orGate1 = Or()
		self.notGate1 = Not()
		
		self.JmpLatch = FlagRegister()
		self.RtnLatch = FlagRegister()
		self.FlagOLatch = FlagRegister()
		self.FlagFLatch = FlagRegister()
		self.SkipLatch = FlagRegister()

		self.DataInRegister = DInRegister()
		self.DataOutRegister = DOutRegister()
		self.ResultRegister = ResultRegister()
		self.InstrRegister = InstrRegister()

		self.instrDecoder = InstrDecoder()
		self.logicUnit = LogicUnit()
		self.mux = Mux()

		self.clockedParts = [self.JmpLatch, self.RtnLatch, self.FlagOLatch, self.FlagFLatch, self.SkipLatch,
							 self.InstrRegister]

		self.resetableParts = [self.JmpLatch, self.RtnLatch, self.FlagOLatch, self.FlagFLatch,
							   self.SkipLatch, self.DataInRegister, self.DataOutRegister,
							   self.ResultRegister, self.InstrRegister]

		super().__init__(numInputs=6, numOutputs=7,
					   name="MC14500 ControlUnit",
					   lines=["Clk", "Data", "I3", "I2", "I1", "I0",
					   		  "Write", "RR", "JMP", "RTN", "FLAG_O", "FLAG_F", "SKIP", "Reset"])
	
		self.addInput(self.Clk)
		self.addInput(self.Data)
		# self.addInput(self.Reset)
		self.addInput(self.I3)
		self.addInput(self.I2)
		self.addInput(self.I1)
		self.addInput(self.I0)

		self.addOutput(self.Write)
		self.addOutput(self.RR)
		self.addOutput(self.JMP)
		self.addOutput(self.RTN)
		self.addOutput(self.FLAG_O)
		self.addOutput(self.FLAG_F)
	
	def Clk(self, *args):
		for clockedPart in self.clockedParts:
			clockedPart.Clk(*args)
		return self.clockedParts[0].Clk(*args)
	
	def Reset(self, *args):
		for resetable in self.resetableParts:
			resetable.Reset(*args)
		return self.resettableParts[0].Reset(*args)
	
	def Data(self, *args):
		self.DataInRegister.Data(*args)
		return self.DataOutRegister.Data(*args)
	
	def I3(self, *args):
		return self.InstrRegister.I3(*args)

	def I2(self, *args):
		return self.InstrRegister.I2(*args)

	def I1(self, *args):
		return self.InstrRegister.I1(*args)

	def I0(self, *args):
		return self.InstrRegister.I0(*args)

	def Write(self, *args):
		return self.andGate3.Q(*args)

	def RR(self, *args):
		return self.notGate1.Q(*args)

	def JMP(self, *args):
		return self.JmpLatch.Q(*args)

	def RTN(self, *args):
		return self.RtnLatch.Q(*args)

	def FLAG_O(self, *args):
		return self.FlagOLatch.Q(*args)

	def FLAG_F(self, *args):
		return self.FlagFLatch.Q(*args)

	def SKIP(self, *args):
		return self.SkipLatch.Q(*args)

	def setInput(self, Clk, Data, I3, I2, I1, I0):
		self.Clk(Clk)
		self.Data(Data)
		self.I3(I3)
		self.I2(I2)
		self.I1(I1)
		self.I0(I0)

	def debugPrint(self, part):
		print("part: {0}".format(part.name))
		print(part.getLineTable())
		print(part)

	def printStates(self):
		self.debugPrint(self)
		self.debugPrint(self.InstrRegister)
		self.debugPrint(self.instrDecoder)
		self.debugPrint(self.DataInRegister)
		self.debugPrint(self.logicUnit)
		self.debugPrint(self.ResultRegister)
		self.debugPrint(self.mux)
		self.debugPrint(self.DataOutRegister)
		self.debugPrint(self.orGate1)
		self.debugPrint(self.andGate1)
		self.debugPrint(self.FlagOLatch)
		print('\n' * 3)

	def process(self):
		self.InstrRegister.process()

		self.instrDecoder.I3(self.InstrRegister.Q3())
		self.instrDecoder.I2(self.InstrRegister.Q2())
		self.instrDecoder.I1(self.InstrRegister.Q1())
		self.instrDecoder.I0(self.InstrRegister.Q0())
		self.instrDecoder.process()

		self.DataInRegister.Clk(self.instrDecoder.IEN())
		self.DataInRegister.process()

		self.andGate2.A(self.Clk())
		self.andGate2.B(self.instrDecoder.LD() 	|
						self.instrDecoder.LDC() |
						self.instrDecoder.AND()	|
						self.instrDecoder.ANDC()|
						self.instrDecoder.OR()	|
						self.instrDecoder.ORC()	|
						self.instrDecoder.XNOR())
		self.andGate2.process()

		self.ResultRegister.Clk(self.andGate2.Q())
								
		self.ResultRegister.process()

		self.logicUnit.Data(self.DataInRegister.Q())
		self.logicUnit.RIn(self.ResultRegister.Q())
		self.logicUnit.LD_OR(self.instrDecoder.LD() | self.instrDecoder.OR())
		self.logicUnit.LDC_ORC(self.instrDecoder.LDC() | self.instrDecoder.ORC())
		self.logicUnit.AND_XNOR(self.instrDecoder.AND() | self.instrDecoder.XNOR())
		self.logicUnit.ANDC(self.instrDecoder.ANDC())
		self.logicUnit.OR_ORC(self.instrDecoder.OR() | self.instrDecoder.ORC())
		self.logicUnit.XNOR(self.instrDecoder.XNOR())
		self.logicUnit.process()

		self.FlagOLatch.Data(self.instrDecoder.NOPO())
		self.FlagOLatch.process()
		self.FlagFLatch.Data(self.instrDecoder.NOPF())
		self.FlagFLatch.process()
		self.SkipLatch.Data(self.instrDecoder.SKZ())
		self.SkipLatch.process()
		self.RtnLatch.Data(self.instrDecoder.RTN())
		self.RtnLatch.process()
		self.JmpLatch.Data(self.instrDecoder.JMP())
		self.JmpLatch.process()

		self.ResultRegister.Data(self.logicUnit.ROut())
		self.ResultRegister.process()

		self.notGate1.A(self.ResultRegister.Qn())
		self.notGate1.process()

		self.mux.A(self.ResultRegister.Q())
		self.mux.B(self.ResultRegister.Qn())
		self.mux.S0(self.instrDecoder.STO())
		self.mux.S1(self.instrDecoder.STOC())
		self.mux.process()

		self.DataOutRegister.Data(self.mux.Q() | self.Data())
		self.DataOutRegister.Clk(self.instrDecoder.OEN())
		self.DataOutRegister.process()

		self.andGate1.A(self.DataOutRegister.Q())
		self.orGate1.A(self.instrDecoder.STO())
		self.orGate1.B(self.instrDecoder.STOC())
		self.orGate1.process()
		self.andGate1.B(self.orGate1.Q())
		self.andGate1.process()

		# Write output is gated with the clock to only be on if the clock is high.
		self.andGate3.A(self.andGate1.Q())
		self.andGate3.B(self.Clk())
		self.andGate3.process()

def TestLU():
	inputTable = [("LD",   [1, 0, 0, 0, 0, 0]), # LD
				  ("OR",   [1, 0, 0, 0, 1, 0]), # OR
				  ("LDC",  [0, 1, 0, 0, 0, 0]), # LDC
				  ("ORC",  [0, 1, 0, 0, 1, 0]), # ORC
				  ("AND",  [0, 0, 1, 0, 0, 0]), # AND
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
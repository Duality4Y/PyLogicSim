from basicparts.Part import Part
from basicparts.Gates import Not, And, Or, Nor, Buffer
from basicparts.FlipFlop import DFlipFlop
from basicparts.Latch import DataLatch

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

class Decoder(Part):
	def __init__(self, lineEncoder3=Buffer(), lineEncoder2=Buffer(), lineEncoder1=Buffer(), lineEncoder0=Buffer()):
		self.lineEncoder0 = lineEncoder0
		self.lineEncoder1 = lineEncoder1
		self.lineEncoder2 = lineEncoder2
		self.lineEncoder3 = lineEncoder3

		self.norGate1 = Nor()
		self.norGate2 = Nor()
		self.andGate = And()

		super().__init__(numInputs=4, numOutputs=1,
						 name="Decoder",
						 lines=["I3", "I2", "I1", "I0", "Q"])
	@property
	def I3(self):
		return self.lineEncoder3.A
	@I3.setter
	def I3(self, value):
		self.lineEncoder3.A = value
	@property
	def I2(self):
		return self.lineEncoder2.A
	@I2.setter
	def I2(self, value):
		self.lineEncoder2.A = value
	@property
	def I1(self):
		return self.lineEncoder1.A
	@I1.setter
	def I1(self, value):
		self.lineEncoder1.A = value
	@property
	def I0(self):
		return self.lineEncoder0.A
	@I0.setter
	def I0(self, value):
		self.lineEncoder0.A = value

	@property
	def Q(self):
		return self.andGate.Q

	def setInput(self, I3, I2, I1, I0):
		self.I3 = I3
		self.I2 = I2
		self.I1 = I1
		self.I0 = I0

	def process(self):
		self.lineEncoder0.process()
		self.lineEncoder1.process()
		self.lineEncoder2.process()
		self.lineEncoder3.process()

		self.norGate1.A = self.lineEncoder0.Q
		self.norGate1.B = self.lineEncoder1.Q
		self.norGate2.A = self.lineEncoder2.Q
		self.norGate2.B = self.lineEncoder3.Q
		self.norGate1.process()
		self.norGate2.process()

		self.andGate.A = self.norGate1.Q
		self.andGate.B = self.norGate2.Q
		self.andGate.process()

	def __repr__(self):
		self.states = [self.I3, self.I2, self.I1, self.I0, self.Q]
		return self.buildTable(self.states)

class InstrDecoder(Part):
	def __init__(self):
		self.decoders = []
		for i in range(0, 16):
			S3 = (i >> 3) & 0x01
			S2 = (i >> 2) & 0x01
			S1 = (i >> 1) & 0x01
			S0 = i & 0x01
			selectLines = [Not() if select else Buffer() for select in [S3, S2, S1, S0]]
			decoder = Decoder(*selectLines)
			self.decoders.append(decoder)

		super().__init__(numInputs=4, numOutputs=16,
						 name="InstrDecoder",
						 lines=["I3", "I2", "I1", "I0",
						 		"NOPO", "LD", "LDC", "AND",
								"ANDC", "OR", "ORC", "XNOR",
								"STO", "STOC", "IEN", "OEN",
								"JMP", "RTN", "SKZ", "NOPF"])
	@property
	def I3(self):
		return self.decoders[0].I3
	@property
	def I2(self):
		return self.decoders[0].I2
	@property
	def I1(self):
		return self.decoders[0].I1
	@property
	def I0(self):
		return self.decoders[0].I0
	@I3.setter
	def I3(self, value):
		for decoder in self.decoders:
			decoder.I3 = value
	@I2.setter
	def I2(self, value):
		for decoder in self.decoders:
			decoder.I2 = value
	@I1.setter
	def I1(self, value):
		for decoder in self.decoders:
			decoder.I1 = value
	@I0.setter
	def I0(self, value):
		for decoder in self.decoders:
			decoder.I0 = value

	@property
	def NOPO(self):
		return self.decoders[0].Q
	@property
	def LD(self):
		return self.decoders[1].Q
	@property
	def LDC(self):
		return self.decoders[2].Q
	@property
	def AND(self):
		return self.decoders[3].Q
	@property
	def ANDC(self):
		return self.decoders[4].Q
	@property
	def OR(self):
		return self.decoders[5].Q
	@property
	def ORC(self):
		return self.decoders[6].Q
	@property
	def XNOR(self):
		return self.decoders[7].Q
	@property
	def STO(self):
		return self.decoders[8].Q
	@property
	def STOC(self):
		return self.decoders[9].Q
	@property
	def IEN(self):
		return self.decoders[10].Q
	@property
	def OEN(self):
		return self.decoders[11].Q
	@property
	def JMP(self):
		return self.decoders[12].Q
	@property
	def RTN(self):
		return self.decoders[13].Q
	@property
	def SKZ(self):
		return self.decoders[14].Q
	@property
	def NOPF(self):
		return self.decoders[15].Q

	def setInput(self, *args):
		for decoder in self.decoders:
			decoder.setInput(*args)

	def process(self):
		for decoder in self.decoders:
			decoder.process()

	def __repr__(self):
		states = [self.I3, self.I2, self.I1, self.I0] + [decoder.Q for decoder in self.decoders]
		return self.buildTable(states)

class Mux(Part):
	def __init__(self):
		self.andGate1 = And()
		self.andGate2 = And()
		self.andGate3 = And()
		self.andGate4 = And()
		self.notGate1 = Not()
		self.notGate2 = Not()
		self.orGate1 = Or()

		super().__init__(numInputs=4, numOutputs=1,
						 name="Mux",
						 lines=["A", "B", "S0", "S1", "Q"])

	@property
	def A(self):
		return self.andGate1.A
	@A.setter
	def A(self, value):
		self.andGate1.A = value
	@property
	def B(self):
		return self.andGate2.B
	@B.setter
	def B(self, value):
		self.andGate2.B = value

	@property
	def S0(self):
		return self.andGate1.B
	@S0.setter
	def S0(self, value):
		self.andGate1.B = value
	@property
	def S1(self):
		return self.andGate4.A
	@S1.setter
	def S1(self, value):
		self.andGate4.A = value
	@property
	def Q(self):
		return self.orGate1.Q

	def setInput(self, A, B, S0, S1):
		self.A = A
		self.B = B
		self.S0 = S0
		self.S1 = S1

	def process(self):
		self.notGate1.A = self.S1
		self.notGate2.A = self.S0
		self.notGate1.process()
		self.notGate2.process()

		self.andGate1.process()
		self.andGate2.A = self.notGate2.Q
		self.andGate2.process()

		self.andGate3.A = self.andGate1.Q
		self.andGate3.B = self.notGate1.Q
		self.andGate3.process()

		self.andGate4.B = self.andGate2.Q
		self.andGate4.process()

		self.orGate1.A = self.andGate3.Q
		self.orGate1.B = self.andGate4.Q
		self.orGate1.process()


	def __repr__(self):
		states = [self.A, self.B, self.S0, self.S1, self.Q]
		return self.buildTable(states)

class InstrRegister(Part):
	def __init__(self):
		self.registers = [DFlipFlop() for i in range(0, 4, 1)]
		super().__init__(numInputs=5, numOutputs=4,
						 name="Instruction Register",
						 lines=["Clk", "I3", "I2", "I1", "I0", "Q3", "Q2", "Q1", "Q0"])
	
	@property
	def Clk(self):
		return self.registers[0].Clk
	@Clk.setter
	def Clk(self, value):
		for register in self.registers:
			register.Clk = value

	@property
	def I0(self):
		return self.registers[0].Data
	@I0.setter
	def I0(self, value):
		self.registers[0].Data = value
	@property
	def I1(self):
		return self.registers[1].Data
	@I1.setter
	def I1(self, value):
		self.registers[1].Data = value
	@property
	def I2(self):
		return self.registers[2].Data
	@I2.setter
	def I2(self, value):
		self.registers[2].Data = value
	@property
	def I3(self):
		return self.registers[3].Data
	@I3.setter
	def I3(self, value):
		self.registers[3].Data = value
	
	@property
	def Q0(self):
		return self.registers[0].Q
	@property
	def Q1(self):
		return self.registers[1].Q
	@property
	def Q2(self):
		return self.registers[2].Q
	@property
	def Q3(self):
		return self.registers[3].Q

	def setInput(self, Clk, I3, I2, I1, I0):
		self.Clk = Clk
		self.I0 = I0
		self.I1 = I1
		self.I2 = I2
		self.I3 = I3

	def process(self):
		for register in self.registers:
			register.process()

	def __repr__(self):
		states = [self.Clk, self.I3, self.I2, self.I1, self.I0, self.Q3, self.Q2, self.Q1, self.Q0]
		return self.buildTable(states)

class DInRegister(Part):
	def __init__(self):
		self.reg = DFlipFlop()
		self.andGate = And()
		self.notGate = Not()
		super().__init__(numInputs=2, numOutputs=1,
						 name="Data In Register",
						 lines=["Clk", "Data", "<Qr>", "Q"])
	@property
	def Data(self):
		return self.reg.Data
	@Data.setter
	def Data(self, value):
		self.reg.Data = value
	
	@property
	def Clk(self):
		return self.notGate.A
	@Clk.setter
	def Clk(self, value):
		self.notGate.A = value

	@property
	def Q(self):
		return self.andGate.Q

	def process(self):
		self.notGate.process()

		self.reg.Clk = self.notGate.Q
		self.reg.process()
		
		self.andGate.A = self.Data
		self.andGate.B = self.reg.Q
		self.andGate.process()

	def __repr__(self):
		states = [self.Clk, self.Data, self.reg.Q, self.Q]
		return self.buildTable(states)

class DOutRegister(Part):
	def __init__(self):
		self.reg = DFlipFlop()
		self.notGate = Not()
		super().__init__(numInputs=2, numOutputs=1,
						 name="Data Out Register",
						 lines=["Data", "CLK", "Q"])
	@property
	def Data(self):
		return self.reg.Data
	@Data.setter
	def Data(self, value):
		self.reg.Data = value
	
	@property
	def Clk(self):
		return self.notGate.A
	@Clk.setter
	def Clk(self, value):
		self.notGate.A = value

	@property
	def Q(self):
		return self.reg.Q

	@property
	def Qn(self):
		return self.reg.Qn

	def process(self):
		self.notGate.process()

		self.reg.Clk = self.notGate.Q
		self.reg.process()

	def __repr__(self):
		states = [self.Data, self.Clk, self.Q]
		return self.buildTable(states)

class FlagRegister(Part):
	def __init__(self):
		self.reg = DataLatch()
		self.notGate = Not()
		super().__init__(numInputs=2, numOutputs=1,
						 name="Flag Register",
						 lines=["Data", "CLK", "Q"])
	@property
	def Data(self):
		return self.reg.Data
	@Data.setter
	def Data(self, value):
		self.reg.Data = value
	
	@property
	def Clk(self):
		return self.notGate.A
	@Clk.setter
	def Clk(self, value):
		self.notGate.A = value

	@property
	def Q(self):
		return self.reg.Q

	@property
	def Qn(self):
		return self.reg.Qn

	def process(self):
		self.notGate.process()

		self.reg.Clk = self.notGate.Q
		self.reg.process()

	def __repr__(self):
		states = [self.Data, self.Clk, self.Q]
		return self.buildTable(states)

class ResultRegister(Part):
	def __init__(self):
		self.reg = DFlipFlop()
		self.andGate = And()
		self.notGate = Not()
		super().__init__(numInputs=2, numOutputs=1,
						 name="ResultRegister",
						 lines=["Clk", "Data", "Q", "Qn"])
	@property
	def Data(self):
		return self.reg.Data
	@Data.setter
	def Data(self, value):
		self.reg.Data = value
	
	@property
	def Clk(self):
		return self.notGate.A
	@Clk.setter
	def Clk(self, value):
		self.notGate.A = value

	@property
	def Q(self):
		return self.reg.Q

	@property
	def Qn(self):
		return self.reg.Qn

	def process(self):
		self.notGate.process()

		self.reg.Clk = self.notGate.Q
		self.reg.process()

	def __repr__(self):
		states = [self.Clk, self.Data, self.Q, self.Qn]
		return self.buildTable(states)

class ControlUnit(Part):
	def __init__(self):
		self.andGate1 = And()
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
							 self.ResultRegister, self.InstrRegister]

		self.resetableParts = [self.JmpLatch, self.RtnLatch, self.FlagOLatch, self.FlagFLatch,
							   self.SkipLatch, self.DataInRegister, self.DataOutRegister,
							   self.ResultRegister, self.InstrRegister]

		super().__init__(numInputs=6, numOutputs=7,
					   name="MC14500 ControlUnit",
					   lines=["Clk", "Data", "I3", "I2", "I1", "I0",
					   		  "Write", "RR", "JMP", "RTN", "FLAG_O", "FLAG_F", "SKIP", "Reset"])
	@property
	def Clk(self):
		return self.JmpLatch.Clk
	@Clk.setter
	def Clk(self, value):
		for clockedPart in self.clockedParts:
			clockedPart.Clk = value

	@property
	def Reset(self):
		return 1
	@Reset.setter
	def Reset(self, value):
		for resetablePart in self.resetableParts:
			resetablePart.Reset = value

	@property
	def Data(self):
		return self.DataInRegister.Data
	@Data.setter
	def Data(self, value):
		self.DataInRegister.Data = value
		self.DataOutRegister.Data = value
	@property
	def I3(self):
		return self.InstrRegister.I3
	@I3.setter
	def I3(self, value):
		self.InstrRegister.I3 = value
	@property
	def I2(self):
		return self.InstrRegister.I2
	@I2.setter
	def I2(self, value):
		self.InstrRegister.I2 = value
	@property
	def I1(self):
		return self.InstrRegister.I1
	@I1.setter
	def I1(self, value):
		self.InstrRegister.I1 = value
	@property
	def I0(self):
		return self.InstrRegister.I0
	@I0.setter
	def I0(self, value):
		self.InstrRegister.I0 = value

	@property
	def Write(self):
		return self.andGate1.Q
	@property
	def RR(self):
		return self.notGate1.Q
	@property
	def JMP(self):
		return self.JmpLatch.Q
	@property
	def RTN(self):
		return self.RtnLatch.Q
	@property
	def FLAG_O(self):
		return self.FlagOLatch.Q
	@property
	def FLAG_F(self):
		return self.FlagFLatch.Q
	@property
	def SKIP(self):
		return self.SkipLatch.Q

	def setInput(self, Clk, Data, I3, I2, I1, I0):
		self.Clk = Clk
		self.Data = Data
		self.I3 = I3
		self.I2 = I2
		self.I1 = I1
		self.I0 = I0

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
		# self.debugPrint(self.FlagOLatch)
		print('\n' * 3)

	def process(self):
		self.InstrRegister.process()

		self.instrDecoder.I3 = self.InstrRegister.Q3
		self.instrDecoder.I2 = self.InstrRegister.Q2
		self.instrDecoder.I1 = self.InstrRegister.Q1
		self.instrDecoder.I0 = self.InstrRegister.Q0
		self.instrDecoder.process()

		self.DataInRegister.Clk = self.instrDecoder.IEN
		self.DataInRegister.process()

		self.logicUnit.Data = self.DataInRegister.Q
		self.logicUnit.RIn = self.ResultRegister.Q
		self.logicUnit.LD_OR = self.instrDecoder.LD | self.instrDecoder.OR
		self.logicUnit.LDC_ORC = self.instrDecoder.LDC | self.instrDecoder.ORC
		self.logicUnit.AND_XNOR = self.instrDecoder.AND | self.instrDecoder.XNOR
		self.logicUnit.ANDC = self.instrDecoder.ANDC
		self.logicUnit.OR_ORC = self.instrDecoder.OR | self.instrDecoder.ORC
		self.logicUnit.XNOR = self.instrDecoder.XNOR
		self.logicUnit.process()

		self.FlagOLatch.Data = self.instrDecoder.NOPO
		self.FlagOLatch.process()
		self.FlagFLatch.Data = self.instrDecoder.NOPF
		self.FlagFLatch.process()
		self.SkipLatch.Data = self.instrDecoder.SKZ
		self.SkipLatch.process()
		self.RtnLatch.Data = self.instrDecoder.RTN
		self.RtnLatch.process()
		self.JmpLatch.Data = self.instrDecoder.JMP
		self.JmpLatch.process()

		self.ResultRegister.Data = self.logicUnit.ROut
		self.ResultRegister.process()

		self.notGate1.A = self.ResultRegister.Qn
		self.notGate1.process()

		self.mux.A = self.ResultRegister.Q
		self.mux.B = self.ResultRegister.Qn
		self.mux.S0 = self.instrDecoder.STO
		self.mux.S1 = self.instrDecoder.STOC
		self.mux.process()

		self.DataOutRegister.Data = self.mux.Q | self.Data
		self.DataOutRegister.Clk = self.instrDecoder.OEN
		self.DataOutRegister.process()

		self.andGate1.A = self.DataOutRegister.Q
		self.orGate1.A = self.instrDecoder.STO
		self.orGate1.B = self.instrDecoder.STOC
		self.orGate1.process()
		self.andGate1.B = self.orGate1.Q
		self.andGate1.process()


	def __repr__(self):
		states = [self.Clk, self.Data, self.I3, self.I2, self.I1, self.I0,
				  self.Write, self.RR, self.JMP, self.RTN, self.FLAG_O, self.FLAG_F, self.SKIP, self.Reset]
		return self.buildTable(states)


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
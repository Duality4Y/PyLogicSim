from basicparts.Part import Part
from basicparts.Gates import And, Or, Not, Buffer, Nand, Nor, Xor, Xnor
from basicparts.Latch import SRLatch, GatedLatch, DataLatch
from basicparts.FlipFlop import FlipFlop, DFlipFlop, TFlipFlop
from basicparts.Adder import HalfAdder, FullAdder
from basicparts.Mux import Mux, DeMux, TestMux
from basicparts.Encoder import Decoder

from utils.TestUtils import testPart, testFlipFlop
from utils.TestUtils import numToBits, clockPart

from devices.MC14K5 import MC14K5

from interface.ui import TestApp

"""
	inputs: Clk
	outputs: Q0 ... Q3
"""
class NibleCounter(Part):
	def __init__(self, *args, **kwargs):
		super().__init__(name=NibleCounter.__name__)

		self.flipflops = [DFlipFlop() for i in range(0, 4)]

		self.addInput(self.Clk)
		self.addOutput(self.Q0)
		self.addOutput(self.Q1)
		self.addOutput(self.Q2)
		self.addOutput(self.Q3)

	def Clk(self, *args):
		return self.flipflops[0].Clk(*args)
	
	def Q0(self, *args):
		return self.flipflops[0].Q(*args)
	
	def Q1(self, *args):
		return self.flipflops[1].Q(*args)
	
	def Q2(self, *args):
		return self.flipflops[2].Q(*args)
	
	def Q3(self, *args):
		return self.flipflops[3].Q(*args)
	
	def setInput(self, Clk):
		self.Clk(Clk)

	def getOutput(self):
		return (self.Q0(), self.Q1(), self.Q2(), self.Q3())
	
	def process(self):
		self.flipflops[0].Data(self.flipflops[0].Qn())
		self.flipflops[0].process()

		self.flipflops[1].Data(self.flipflops[1].Qn())
		self.flipflops[1].Clk(self.flipflops[0].Q())
		self.flipflops[1].process()

		self.flipflops[2].Data(self.flipflops[2].Qn())
		self.flipflops[2].Clk(self.flipflops[1].Q())
		self.flipflops[2].process()
		
		self.flipflops[3].Data(self.flipflops[3].Qn())
		self.flipflops[3].Clk(self.flipflops[2].Q())
		self.flipflops[3].process()

def testCounter(part):
	print("Testing '{0}' part.".format(part.name))
	print(counter.getLineTable())
	for i in range(0, 2 ** counter.numOutputs):
		counter.Clk(1)
		counter.process()
		print(counter)
		counter.Clk(0)
		counter.process()
		print(counter)
	print()

if __name__ == "__main__":
	app = TestApp()
	app.run()
	exit()

	testPart(And())
	testPart(Or())
	testPart(Not())
	testPart(Buffer())
	testPart(Nand())
	testPart(Nor())
	testPart(Xor())
	testPart(Xnor())

	testPart(SRLatch())
	testPart(GatedLatch())
	testPart(DataLatch())

	testPart(HalfAdder())
	testPart(FullAdder())

	testFlipFlop(FlipFlop())
	testFlipFlop(DFlipFlop())
	testFlipFlop(TFlipFlop())

	testPart(Decoder())
	TestMux(Mux())
	testPart(DeMux())

	MC14K5.TestLU()

	testPart(MC14K5.Decoder())
	testPart(MC14K5.Mux())
	testPart(MC14K5.InstrDecoder())
	testFlipFlop(MC14K5.InstrRegister())
	testFlipFlop(MC14K5.DInRegister())
	testFlipFlop(MC14K5.DOutRegister())
	testFlipFlop(MC14K5.FlagRegister())
	testFlipFlop(MC14K5.ResultRegister())
	testPart(MC14K5.ControlUnit())

	instr = MC14K5.Instructions()
	control = MC14K5.ControlUnit()

	print("-> input enable.")
	control.setInput(0, 1, *numToBits(4, instr.IEN))
	clockPart(control)
	print("-> LD(1) and STO(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)
	print("-> LD(0) and STO(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)

	print("-> LD(1) and STOC(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockPart(control)
	print("-> LD(0) and STOC(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockPart(control)

	print("-> output enable.")
	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockPart(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockPart(control)


	print("-> write 1 through loading zero and storing the complement.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPO))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPF))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.SKZ))
	clockPart(control)

	control.setInput(0, 1, *numToBits(4, instr.RTN))
	clockPart(control)
	
	control.setInput(0, 1, *numToBits(4, instr.JMP))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.STO))
	clockPart(control)

	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockPart(control)

	counter = NibleCounter()
	testCounter(counter)
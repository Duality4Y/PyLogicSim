from Part import Part
from Gates import And, Or, Not, Buffer, Nand, Nor, Xor, Xnor
from Latch import SRLatch, GatedLatch, DataLatch
from FlipFlop import FlipFlop, DFlipFlop, TFlipFlop
from Adder import HalfAdder, FullAdder

from Mux import Mux, DeMux, TestMux
from Encoder import Decoder

from TestUtils import TestPart, TestFlipFlop

import MC14K5

if __name__ == "__main__":
	print("Hello, world!")

	TestPart(And())
	TestPart(Or())
	TestPart(Not())
	TestPart(Buffer())
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

	TestPart(Decoder())
	TestMux(Mux())
	TestPart(DeMux())

	def numToBits(length, number):
		return [(number >> (length - i - 1)) & 0x01 for i in range(0, length)]

	def clockMC14K5(part):
		part.Clk = 1
		part.process()
		part.Clk = 0
		part.process()

		part.printStates()

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
			

	instr = Instructions()

	MC14K5.TestLU()
	TestPart(MC14K5.Decoder())
	TestPart(MC14K5.Mux())
	TestPart(MC14K5.InstrDecoder())
	TestPart(MC14K5.InstrRegister())
	TestFlipFlop(MC14K5.InstrRegister())
	# TestPart(MC14K5.ControlUnit())

	control = MC14K5.ControlUnit()

	print("-> input enable.")
	control.setInput(0, 1, *numToBits(4, instr.IEN))
	clockMC14K5(control)
	print("-> LD(1) and STO(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockMC14K5(control)
	print("-> LD(0) and STO(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockMC14K5(control)

	print("-> LD(1) and STOC(1) test.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockMC14K5(control)
	print("-> LD(0) and STOC(0) test.")
	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 1, *numToBits(4, instr.STOC))
	clockMC14K5(control)

	print("-> output enable.")
	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockMC14K5(control)
	control.setInput(0, 1, *numToBits(4, instr.STO))
	clockMC14K5(control)


	print("-> write 1 through loading zero and storing the complement.")
	control.setInput(0, 1, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockMC14K5(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockMC14K5(control)

	control.setInput(0, 0, *numToBits(4, instr.LD))
	clockMC14K5(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockMC14K5(control)
	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockMC14K5(control)
	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockMC14K5(control)

	control.setInput(0, 0, *numToBits(4, instr.OEN))
	clockMC14K5(control)

	control.setInput(0, 1, *numToBits(4, instr.OEN))
	clockMC14K5(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPO))
	clockMC14K5(control)

	control.setInput(0, 1, *numToBits(4, instr.NOPF))
	clockMC14K5(control)

	control.setInput(0, 1, *numToBits(4, instr.SKZ))
	clockMC14K5(control)

	control.setInput(0, 1, *numToBits(4, instr.RTN))
	clockMC14K5(control)
	
	control.setInput(0, 1, *numToBits(4, instr.JMP))
	clockMC14K5(control)

	control.setInput(0, 0, *numToBits(4, instr.STO))
	clockMC14K5(control)

	control.setInput(0, 0, *numToBits(4, instr.STOC))
	clockMC14K5(control)

	
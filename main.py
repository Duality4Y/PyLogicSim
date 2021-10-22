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

if __name__ == "__main__":
	print("Hello, world!")

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
	testPart(MC14K5.InstrRegister())
	testFlipFlop(MC14K5.InstrRegister())
	# testPart(MC14K5.ControlUnit())

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


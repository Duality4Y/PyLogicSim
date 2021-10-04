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

	MC14K5.TestLU()
	TestPart(MC14K5.Decoder())
	TestPart(MC14K5.Mux())
	TestPart(MC14K5.InstrDecoder())
	TestPart(MC14K5.InstrRegister())
	TestFlipFlop(MC14K5.InstrRegister())
	TestPart(MC14K5.ControlUnit())
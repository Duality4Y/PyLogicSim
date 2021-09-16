from Part import Part
from Gates import And, Or, Not, Nand, Nor, Xor, Xnor
from Latch import SRLatch, GatedLatch, DataLatch
from FlipFlop import FlipFlop, DFlipFlop
from Adder import HalfAdder, FullAdder

from TestUtils import TestPart, TestFlipFlop

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
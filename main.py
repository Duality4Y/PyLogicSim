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

	MC14K5.TestLU()
	TestPart(MC14K5.Decoder())
	TestPart(MC14K5.Mux())
	TestPart(MC14K5.InstrDecoder())
	TestPart(MC14K5.InstrRegister())
	TestFlipFlop(MC14K5.InstrRegister())
	# TestPart(MC14K5.ControlUnit())
	control = MC14K5.ControlUnit()

	print("Input Enable by setting data and giving the IEN instruction")
	control.setInput(0, 1, *numToBits(4, 10))
	clockMC14K5(control)
	print("different instruction so that IEN will fall low and clock in data.")
	control.setInput(0, 1, *numToBits(4, 0))
	clockMC14K5(control)

	print("execute OR so that result of LU will be 1 and see if we can clock it into the RR register.")
	control.setInput(0, 1, *numToBits(4, 5))
	clockMC14K5(control)
	print("another clock pulse to actually put it in the ResultRegister")
	clockMC14K5(control)
	# control.setInput(0, 1, *numToBits(4, 0))
	# clockMC14K5(control)

from basicGates import And, Or, Not, Nand, Nor, Xor, Xnor

# class 

def TestGate(gate):
	print(f"gate: {gate.__class__.__name__}")
	if gate.numInputs == 1:
		print("A | Q")
	else:
		print("A | B | Q")

	for i in range(0, 2 ** gate.numInputs):
		
		inValues = []
		for bitPos in range(0, gate.numInputs):
			inValues.insert(0, (i >> bitPos) & 0x01)
		
		gate.setInput(*inValues)
		gate.process()
		
		print(gate)


if __name__ == "__main__":
	print("Hello, world!")
	TestGate(And())
	TestGate(Or())
	TestGate(Not())
	TestGate(Nand())
	TestGate(Nor())
	TestGate(Xor())
	TestGate(Xnor())
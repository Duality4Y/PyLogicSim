def getPulseShape(risingPulse):
	return [0, 1, 0] if risingPulse else [1, 0, 1]

def TestPart(part):
	print("Testing '{0}' part.".format(part.name))
	print(part.getLineTable())
	for i in range(0, 2 ** part.numInputs):
		inValues = []
		for bitPos in range(0, part.numInputs):
			inValues.insert(0, (i >> bitPos) & 0x01)
		part.setInput(*inValues)
		part.process()
		print(part)
	print()

def ToggleClk(part, risingPulse=True):
	pulseShape = getPulseShape(risingPulse)
	for clkstate in pulseShape:
		if hasattr(part, "Clk"):
			part.Clk = clkstate # normal flipflops have a clk input
		elif hasattr(part, "T"):
			part.T = clkstate # toggle flipflop has a T which is basically a clock input too
		part.process()
		print(part)

def TestFlipFlop(part):
	print("Testing '{0}' part.".format(part.name))
	for i in range(0, 2 ** (part.numInputs)):
		inValues = []
		for bitPos in range(0, part.numInputs):
			inValues.insert(0, (i >> bitPos) & 0x01)
		part.setInput(*inValues)
		print(part.getLineTable())
		ToggleClk(part)
	print()
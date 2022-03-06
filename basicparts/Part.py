"""
	Basic class for description of a part
	like how many inputs and outputs it has
	and what the names are of those inputs/outputs
	and what the name is for that part.

	e.g. a And gate has 2 inputs and 1 output
	and a latch 2 inputs and 2 outputs.

	by making this a class to be inherited from 
	you could use it to dynamically generate tests or do other things with it.
"""

class Part(object):
	# def __init__(self, numInputs=0, numOutputs=0, name="Unknown", lines=["Not", "available"]):
	def __init__(self, *args, **kwargs):
		self.inputs = []		# only an input
		self.outputs = []		# only an output 
		self.inputOutputs = []	# both input and output
		
		self._name = kwargs.get("name", "Unknown")
		self.lines = []

		self._alignsize = 0
		self._fmt = ""
		self._tableSeperator = "|"

	@property
	def name(self):
		return self._name
	
	@property
	def numInputs(self):
		return len(self.inputs)
	
	@property
	def numOutputs(self):
		return len(self.outputs)
	
	@property
	def numInputOutputs(self):
		return len(self.inputOutputs)

	@property
	def lineTable(self):
		return self.buildTable(self.lines)

	def buildTable(self, elements):
		return self._tableSeperator.join(self._fmt.format(str(element)) for element in elements)

	def updateTable(self):
		self._alignsize = max(len(item) for item in self.lines) + 1
		self._fmt = "{{0:{0}}}".format(self._alignsize)

	def addLine(self, io, lineName=None):
		name = lineName if lineName else io.__name__
		self.lines.append(name)
	
	def addInput(self, input, name=None):
		self.inputs.append(input)
		self.addLine(input, lineName=name)
		self.updateTable()

	def addOutput(self, output, name=None):
		self.outputs.append(output)
		self.addLine(output, lineName=name)
		self.updateTable()
	
	def addInputOutput(self, inputOutput, name=None):
		self.inputOutputs.append(inputOutput)
		self.addLine(inputOutput, lineName=name)
		self.updateTable()

	def __repr__(self):
		states = [state() for state in (*self.inputs, *self.inputOutputs, *self.outputs)]
		return self.buildTable(states)
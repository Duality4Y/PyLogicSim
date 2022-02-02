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
		self.inputs = []
		self.outputs = []
		
		self._name = kwargs.get("name", "Unknown")
		# self.lines = kwargs.get("lines", ["Not", "available"])
		self.lines = []

		self._alignsize = 0
		self._fmt = ""
		self._tableSeperator = "|"
	
	@property
	def numInputs(self):
		return len(self.inputs)
	
	@property
	def numOutputs(self):
		return len(self.outputs)

	def updateTable(self):
		self._alignsize = max(len(item) for item in self.lines) + 1
		self._fmt = "{{0:{0}}}".format(self._alignsize)

	def updateLines(self):
		self.lines = []
		for io in (*self.inputs, *self.outputs):
			self.lines.append(io.__name__)

	@property
	def name(self):
		return self._name

	def buildTable(self, elements):
		return self._tableSeperator.join(self._fmt.format(str(element)) for element in elements)

	def getLineTable(self):
		return self.buildTable(self.lines)
	
	def addInput(self, input):
		self.inputs.append(input)
		self.updateLines()
		self.updateTable()

	def addOutput(self, output):
		self.outputs.append(output)
		self.updateLines()
		self.updateTable()

	def process(self):
		pass

	def __repr__(self):
		states = [state() for state in (*self.inputs, *self.outputs)]
		return self.buildTable(states)
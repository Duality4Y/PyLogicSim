from basicparts.Part import Part

class FMemory(Part):
	def __init__(self, addrWidth=13, dataWidth=8):
		super().__init__(name="Memory")
		self.dataList = {}
		self.address = 0
		self.data = 0
		self.size = 2 ** addrWidth

		self.dataWidth = dataWidth
		self.addrWidth = addrWidth

		self.dataFuncBitPos = {}
		self.addrFuncBitPos = {}
		
		self._WE = 1
		self.addInput(self.WE)

		for addr in range(0, self.size):
			self.dataList[addr] = 0
		
		for i in range(0, addrWidth)[::-1]:
			addrFuncStr = f"A{i}"
			addrFunc = getattr(self, addrFuncStr)
			self.addInput(addrFunc, name=addrFuncStr)
			self.addrFuncBitPos[addrFuncStr] = i

		for i in range(0, dataWidth)[::-1]:
			dataFuncStr = f"D{i}"
			dataFunc = getattr(self, dataFuncStr)
			self.addInputOutput(dataFunc, name=dataFuncStr)
			self.dataFuncBitPos[dataFuncStr] = i
		

	def WE(self, *args):
		if args: self._WE = args[0]
		return self._WE
	
	def setInput(self, addrBits, dataBits=None):

		for i, v in enumerate(addrBits[::-1]):
			addrFuncStr = f"A{i}"
			addrFunc = getattr(self, addrFuncStr)
			addrFunc(v)

		if dataBits:
			for i, v in enumerate(dataBits[::-1]):
				dataFuncStr = f"D{i}"
				dataFunc = getattr(self, dataFuncStr)
				dataFunc(v)
	
	def process(self):
		if self.WE() == 0:
			self.dataList[self.address] = self.data
		else:
			self.data = self.dataList[self.address]
	
	def __getattr__(self, name):
		def addrBit(*args):
			bit = self.addrFuncBitPos[addrBit.__name__]
			if args:
				if args[0]:
					self.address |= (1 << bit)
				else:
					self.address &= ~(1 << bit)
			return 1 if self.address & (1 << bit) else 0

		def dataBit(*args):
			bit = self.dataFuncBitPos[dataBit.__name__]
			if args:
				if args[0]:
					self.data |= (1 << bit)
				else:
					self.data &= ~(1<< bit)
			return 1 if self.data & (1 << bit) else 0
		
		if name.startswith('D'):
			dataBit.__name__ = name
			dataBit.__qualname__ = __class__.__qualname__ + '.' + name
			return dataBit
		elif name.startswith('A'):
			addrBit.__name__ = name
			addrBit.__qualname__ = __class__.__qualname__ + '.' + name
			return addrBit
		
		return object.__getattribute__(self, name)
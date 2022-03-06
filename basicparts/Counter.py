from basicparts.Part import Part
from basicparts.FlipFlop import DFlipFlop
from basicparts.Gates import And

class NibbleCounter(Part):
	def __init__(self, *args, **kwargs):
		super().__init__(name=NibbleCounter.__name__)

		self.flipflops = [DFlipFlop() for i in range(0, 4)]

		self.and1 = And()
		self.and2 = And()
		self.and3 = And()

		self.addInput(self.Clk)
		self.addOutput(self.Co)
		self.addOutput(self.Q0)
		self.addOutput(self.Q1)
		self.addOutput(self.Q2)
		self.addOutput(self.Q3)

	def Clk(self, *args):
		return self.flipflops[0].Clk(*args)
	
	def Co(self, *args):
		return self.and3.Q(*args)
	
	def Q0(self, *args):
		return self.flipflops[0].Q(*args)
	
	def Q1(self, *args):
		return self.flipflops[1].Q(*args)
	
	def Q2(self, *args):
		return self.flipflops[2].Q(*args)
	
	def Q3(self, *args):
		return self.flipflops[3].Q(*args)
	
	def setInput(self, Clk):
		self.Clk(Clk)

	def getOutput(self):
		return (self.Co(), self.Q0(), self.Q1(), self.Q2(), self.Q3())
	
	def process(self):
		prevFlipflop = None
		for flipflop in self.flipflops:
			if prevFlipflop:
				flipflop.Clk(prevFlipflop.Q())
			flipflop.Data(flipflop.Qn())
			flipflop.process()

			prevFlipflop = flipflop

		self.and1.A(self.Q0())
		self.and1.B(self.Q1())
		self.and2.A(self.Q2())
		self.and2.B(self.Q3())
		self.and1.process()
		self.and2.process()

		self.and3.A(self.and1.Q())
		self.and3.B(self.and2.Q())
		self.and3.process()

class ByteCounter(Part):
	def __init__(self, *args, **kwargs):
		super().__init__(name=ByteCounter.__name__)

		self.and1 = And()

		self.counter1 = NibbleCounter()
		self.counter2 = NibbleCounter()

		self.addInput(self.Clk)
		self.addOutput(self.Co)
		self.addOutput(self.Q0)
		self.addOutput(self.Q1)
		self.addOutput(self.Q2)
		self.addOutput(self.Q3)
		self.addOutput(self.Q4)
		self.addOutput(self.Q5)
		self.addOutput(self.Q6)
		self.addOutput(self.Q7)
		
	def Clk(self, *args):
		return self.counter1.Clk(*args)
	
	def Co(self, *args):
		return self.and1.Q(*args)
	
	def Q0(self, *args):
		return self.counter1.Q0(*args)
	
	def Q1(self, *args):
		return self.counter1.Q1(*args)
	
	def Q2(self, *args):
		return self.counter1.Q2(*args)
	
	def Q3(self, *args):
		return self.counter1.Q3(*args)

	def Q4(self, *args):
		return self.counter2.Q0(*args)
	
	def Q5(self, *args):
		return self.counter2.Q1(*args)
	
	def Q6(self, *args):
		return self.counter2.Q2(*args)
	
	def Q7(self, *args):
		return self.counter2.Q3(*args)
	
	def setInput(self, Clk):
		self.Clk(Clk)
	
	def getOutput(self):
		return (self.Co(), self.Q0(), self.Q1(),
						   self.Q2(), self.Q3(),
						   self.Q4(), self.Q5(),
						   self.Q6(), self.Q7())
	
	def process(self):
		self.counter1.process()
		self.counter2.Clk(self.counter1.Co())
		self.counter2.process()

		self.and1.A(self.counter1.Co())
		self.and1.B(self.counter2.Co())
		self.and1.process()
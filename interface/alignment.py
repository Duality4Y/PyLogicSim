
class Alignment(object):
	(CENTER,
	 LEFT,
	 RIGHT) = [i for i in range(0, 3)]
	def __init__(self, *args, **kwargs):
		self.type = kwargs.get("type", Alignment.LEFT)
	
	"""
		calculate rect2 alignment relative to rect1 with padding
	"""
	def apply(self, rect1, rect2):
		lx, ly, lwidth, lheight = rect1
		tx, ty, twidth, theight = rect2
		if self.type == Alignment.CENTER:
			x = int(lx + (lwidth - twidth) / 2)
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		elif self.type == Alignment.LEFT:
			x = lx
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		elif self.type == Alignment.RIGHT:
			x = lx + (lwidth - twidth)
			y = int(ly + (lheight - theight) / 2)
			return (x, y) 
		return (0, 0)

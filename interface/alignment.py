

class Alignment(object):
	(CENTER,
	 LEFT,
	 RIGHT) = [i for i in range(0, 3)]
	def __init__(self):
		pass
	"""
		calculate rect2 alignment relative to rect1 with padding
	"""
	def apply(self, rect1, rect2, alignment, padding):
		lx, ly, lwidth, lheight = rect1
		tx, ty, twidth, theight = rect2
		if alignment == Alignment.CENTER:
			x = int(lx + (lwidth - twidth) / 2)
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == Alignment.LEFT:
			x = lx + padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y)
		if alignment == Alignment.RIGHT:
			x = lx + (lwidth - twidth) - padding
			y = int(ly + (lheight - theight) / 2)
			return (x, y) 
		return (0, 0)
Alignment = Alignment()

"""
	check if rect2 collides with rect1
"""
def CheckCollision(rect1, rect2):
	x1, y1, width1, height1 = rect1
	x2, y2, _, _ = rect2

	if (x2 > x1 and x2 < (x1 + width1)) and (y2 > y1 and y2 < (y1 + height1)):
		return True
	return False

"""
	return a area rectangle that is bigger then rect by adding size * 2 amount to width and height.
"""
def expandArea(areaRect, size=2, centered=True):
	if centered:
		x, y, width, height = areaRect
		x = x - size
		y = y - size
		width = width + (2 * size)
		height = height + (2 * size)
		return x, y, width, height
	else:
		return (1, 1, 1, 1)

"""
	return a area rectangle that is bigger then rect by adding size * 2 amount to width and height.
"""
def shrinkArea(areaRect, size=2, centered=True):
	if centered:
		x, y, width, height = areaRect
		x = x + size
		y = y + size
		width = width - (2 * size)
		height = height - (2 * size)
		return x, y, width, height
	else:
		return (1, 1, 1, 1)

def setAreaPosition(pos, rect):
	_, _, width, height = rect
	pX, pY = pos
	return *pos, width, height

def getAreaPosition(rect):
	x, y, width, height = rect
	return (x, y)

def setAreaSize(size, rect):
	x, y, width, height = rect
	return x, y, *size

def getAreaSize(rect):
	_, _, width, height = rect
	return width, height
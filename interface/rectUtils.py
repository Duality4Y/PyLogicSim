
"""
	check if rect2 collides with rect1
"""
def CheckCollision(rect1, rect2):
	x1, y1, width1, height1 = rect1
	x2, y2, _, _ = rect2

	if (x2 > x1 and x2 < (x1 + width1)) and (y2 > y1 and y2 < (y1 + height1)):
		return True
	return False
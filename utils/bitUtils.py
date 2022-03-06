def numToBits(length, number):
	return [(number >> (length - i - 1)) & 0x01 for i in range(0, length)]
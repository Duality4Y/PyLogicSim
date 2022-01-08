import pygame

from interface.window import UIFont
from interface.widget import Widget
from interface.alignment import Alignment

from interface.colorDefs import *

class Label(Widget):
	# def __init__(self, text="", textAlignment=Alignment.center, borderVisible=True):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.text = kwargs.get('text', "")
		# self.textColor = WHITE
		self.textColor = tuple([0xff] * 3)
		self.border = 2
		self.borderColor = BLUE

		self.borderVisible = kwargs.get('borderVisible', True)

		# how much room between edge and text (padding between text and label border)
		self.defaultPadding = 8
		self.padding = self.defaultPadding

		self.textAlignment = kwargs.get('textAlignment', Alignment.CENTER)
		self.textSurface, self.textRect = UIFont.render(self.text, self.textColor)
		_, _, textWidth, textHeight = self.textRect
		self.rect = (0, 0, textWidth * 1.5 + self.defaultPadding, textHeight * 1.5 + self.defaultPadding)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			pygame.draw.rect(surface, self.borderColor, self.applyOffset(self.rect), self.border)
	
	def draw(self, surface):
		""" Draw the text after applying a alignment function to its position. """
		x, y = Alignment.apply(self.applyOffset(self.rect), self.textRect, self.textAlignment, self.padding)
		surface.blit(self.textSurface, (x, y))
		""" draw a border """
		self.drawBorder(surface)
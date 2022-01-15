import pygame

from interface.window import UIFont, fontSize
from interface.widget import Widget
# from interface.alignment import Alignment
from interface.alignment import Alignment

from interface.colorDefs import *

class Label(Widget):
	# def __init__(self, text="", textAlignment=Alignment.center, borderVisible=True):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.text = kwargs.get('text', "")
		self.borderVisible = kwargs.get('borderVisible', True)

		self.textColor = tuple([0xff] * 3)
		self.textSurface, self.textSurfaceRect = UIFont.render(self.text, self.textColor, size=fontSize)
		_, _, textWidth, textHeight = self.textSurfaceRect
		self.contentArea = 0, 0, textWidth, textHeight
		
		self.alignment = Alignment(type=kwargs.get("textAlign", Alignment.CENTER))
	
	def update(self):
		super().update()

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			pygame.draw.rect(surface, self.borderColor, self.borderArea, self.borderFill)

	def drawContent(self, surface):
		""" Draw the text after applying a alignment function to its position. """
		x, y = self.alignment.apply(self.contentArea, self.textSurfaceRect)
		surface.blit(self.textSurface, (x, y))

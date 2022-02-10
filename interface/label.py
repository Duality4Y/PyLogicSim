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

		self.text = kwargs.get("text", "")
		self.textColor = kwargs.get("textColor", (0xFF, 0xFF, 0xFF))
		self.textHighlightSize = kwargs.get("highlighSize", 2)

		self.borderVisible = kwargs.get('borderVisible', True)

		self.textSurface, self.textSurfaceRect = UIFont.render(self.text, self.textColor, size=fontSize)
		_, _, textWidth, textHeight = self.textSurfaceRect
		self.contentArea = 0, 0, textWidth, textHeight

		self.textBgSurface, self.textBgSurfaceRect = UIFont.render(self.text, (0x00, 0x00, 0x00), size=fontSize)
		self.textBgSurface.set_alpha(0x80)

		self.alignment = Alignment(type=kwargs.get("textAlign", Alignment.CENTER))
	
	def update(self):
		super().update()

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			pygame.draw.rect(surface, self.borderColor, self.borderArea, self.borderFill)

	def drawTextHighlight(self, surface):
		x, y = self.alignment.apply(self.contentArea, self.textBgSurfaceRect)
		for i in range(0, self.textHighlightSize):
			surface.blit(self.textBgSurface, (x+i, y))
			surface.blit(self.textBgSurface, (x-i, y))
			surface.blit(self.textBgSurface, (x, y+i))
			surface.blit(self.textBgSurface, (x, y-i))

			surface.blit(self.textBgSurface, (x-i, y-i))
			surface.blit(self.textBgSurface, (x-i, y+i))
			surface.blit(self.textBgSurface, (x+i, y-i))
			surface.blit(self.textBgSurface, (x+i, y+i))
		
	def drawContent(self, surface):
		""" Draw the text after applying a alignment function to its position. """
		self.drawTextHighlight(surface)
		x, y = self.alignment.apply(self.contentArea, self.textSurfaceRect)
		surface.blit(self.textSurface, (x, y))

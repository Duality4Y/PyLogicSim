import pygame

from interface.label import Label
from interface.alignment import Alignment
from interface.rectUtils import CheckCollision

from interface.colorDefs import *

class Button(Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.mpos = 0, 0

		""" Custom label properties for a button. """
		self.textAlignment = kwargs.get("textAlignment", Alignment.CENTER)

		self.clickState = 0
		self.prevClickState = 0

		self.onPressed = None
		self.onReleased = None

		self.pressedCallback = None
		self.releasedCallback = None

		self.selectedColor = (0, 0xff >> 1, 0)

		self.mouseHover = False
		self.hoverColor = (0x66, 0x99, 0xCC)
		self.isHeld = False

	def setClickState(self, clickState):
		self.clickState = clickState

	def isPressed(self):
		return (self.clickState > self.prevClickState)

	def isReleased(self):
		return (self.clickState < self.prevClickState)

	def drawBorder(self, surface):
		""" Draw a border rectangular. """
		if(self.borderVisible):
			x, y, width, height = self.borderArea
			smallest = min(width, height)
			
			borderColor = self.borderColor
			if self.mouseHover:
				borderColor = self.hoverColor
			
			pygame.draw.rect(surface, borderColor, self.borderArea, self.borderFill, round(smallest / 3))

	def drawContent(self, surface):
		""" Draw a highlight when held down. """
		if self.isHeld:
			if(self.borderVisible):
				x, y, width, height = self.contentArea
				smallest = min(width, height)
				pygame.draw.rect(surface, self.selectedColor, self.contentArea, 0, round(smallest / 3))
		super().drawContent(surface)


	def handleEvents(self, event):
		leftMouseBtn, _, _ = pygame.mouse.get_pressed()
		self.setClickState(leftMouseBtn)
		if event.type == pygame.MOUSEMOTION:
			self.mpos = event.pos

	def processEvents(self):
		self.mouseHover = CheckCollision(self.contentArea, (*self.mpos, 0, 0))
		if self.mouseHover:
			if self.isPressed():
				self.isHeld = True
				if self.pressedCallback:
					self.pressedCallback(self)
			if self.isReleased():
				self.debugPrintParents()
				if self.releasedCallback:
					self.releasedCallback(self)
		""" update button state when mouse not on it but still releases button """
		if self.isReleased():
			self.isHeld = False
		self.prevClickState = self.clickState

class CheckButton(Button):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.marked = False
		self.prevMarked = False

		self.checkCallback = None
		self.releasedCallback = self.toggleMarked

	def toggleMarked(self, widget):
		self.marked = not self.marked

	def drawContent(self, surface):
		""" fill in the button if button is set. """
		if(self.marked):
			if(self.borderVisible):
				x, y, width, height = self.contentArea
				smallest = min(width, height)
				pygame.draw.rect(surface, self.selectedColor, self.contentArea, 0, round(smallest / 3))
		""" Draw the normal border to indicate it's a button. """
		super().drawContent(surface)

	def processEvents(self):
		super().processEvents()
		if self.prevMarked != self.marked:
			if self.checkCallback:
				self.checkCallback(self)
		self.prevMarked = self.marked
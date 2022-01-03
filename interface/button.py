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
		self.borderPadding = self.border * 2
		_, _, textWidth, textHeight = self.textRect
		self.rect = (50, 50, textWidth * 1.5 + self.defaultPadding + self.borderPadding + 200, textHeight * 1.5 + self.defaultPadding + self.borderPadding)
		self.borderColor = [169] * 3
		self.textAlignment = kwargs.get("textAlignment", Alignment.RIGHT)

		self.clickState = 0
		self.prevClickState = 0

		self.onPressed = None
		self.onReleased = None

		self.pressedCallback = None
		self.releasedCallback = None

		"""
			if highLightBorder has a value high then zero an highlight border that size is draw
			if highLightBorder is zero then the rect is filled.

			used for indicating a button is set or pressed down.
		"""
		self.highLightBorder = 0

		self.highLightColor = GREEN
		self.highLightColor = (0, 0xff >> 1, 0)

		self.colliding = False
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
			x, y, width, height = self.rect
			smallest = min(width, height)
			marginSize = 10
			marginRect = x + marginSize, y + marginSize, width - marginSize * 2, height - marginSize * 2
			pygame.draw.rect(surface, self.borderColor, self.applyOffset(marginRect), self.border, round(smallest / 3))

	def draw(self, surface):
		""" Draw a highlight when held down. """
		if self.isHeld:
			if(self.borderVisible):
				x, y, width, height = self.rect
				smallest = min(width, height)
				marginSize = 10
				marginRect = x + marginSize, y + marginSize, width - marginSize * 2, height - marginSize * 2
				pygame.draw.rect(surface, self.highLightColor, self.applyOffset(marginRect), self.highLightBorder, round(smallest / 3))

		super().draw(surface)

	def handleEvents(self, event):
		leftMouseBtn, _, _ = pygame.mouse.get_pressed()
		self.setClickState(leftMouseBtn)
		if event.type == pygame.MOUSEMOTION:
			self.mpos = event.pos

	def processEvents(self):
		self.colliding = CheckCollision(self.applyOffset(self.rect), (*self.mpos, 0, 0))
		if self.colliding:
			if self.isPressed():
				self.isHeld = True
				if self.pressedCallback:
					self.pressedCallback(self)
			if self.isReleased():
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

	def draw(self, surface):
		""" fill in the button if button is set. """
		if(self.marked):
			if(self.borderVisible):
				_, _, width, height = self.rect
				smallest = min(width, height)
				pygame.draw.rect(surface, self.highLightColor, self.applyOffset(self.rect), self.highLightBorder, round(smallest / 3))
		""" Draw the normal border to indicate it's a button. """
		super().draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)

	def processEvents(self):
		super().processEvents()
		if self.prevMarked != self.marked:
			if self.checkCallback:
				self.checkCallback(self)
		self.prevMarked = self.marked
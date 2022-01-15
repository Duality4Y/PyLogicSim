import pygame

from interface.widget import Widget

from interface.rectUtils import *
from interface.colorDefs import *

class Container(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.widgets = []

	def addWidget(self, widget):
		widget.setParent(self)
		self.widgets.append(widget)

	def update(self):
		"""
			simply delegate updating to the widget specific updating code may be implemented in different containers
			which have different ways of dividing up the space for the widgets.
		"""
		super().update()
		for widget in self.widgets:
			widget.update()

	""" Draw all the widgets in the Container. """
	def draw(self, surface):
		super().draw(surface)
		for widget in self.widgets:
			widget.draw(surface)

	def handleEvents(self, event):
		super().handleEvents(event)
		for widget in self.widgets:
			widget.handleEvents(event)

	def processEvents(self):
		super().processEvents()
		for widget in self.widgets:
			widget.processEvents()

class Pane(Container):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.borderVisible = True

		self.borderColor = (0x90, 0xEE, 0x90)
		self.borderFill = 1
		self.borderSize = 4
	
	def update(self):
		super().update()
		for widget in self.widgets:
			widget.assignArea(self.contentArea)
			widget.update()

	def drawBorder(self, surface):
		if self.borderVisible:
			# outer border is easy to draw it is just the bounding rectangle of the border.
			pygame.draw.rect(surface, self.borderColor, self.borderArea, self.borderFill)
			# the inner is just the outer but shrunk down made it conditional so it looks nicer.
			if self.borderSize:
				inner = shrinkArea(self.borderArea, self.borderSize - 1)
			else:
				inner = shrinkArea(self.borderArea, self.borderSize)
			pygame.draw.rect(surface, self.borderColor, inner, self.borderFill, border_radius=10)

class Grid(Widget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.layout = [[]]
		self.rect = (0, 0, 0, 0)

	def addRow(self, widget, pos=0, size=1):
		self.layout[pos].append(widget)

	def addCol(self, widget, pos=0, size=1):
		pass

	def draw(self, surface):
		for row in self.layout:
			for widget in row:
				# set it's position
				widget.draw(surface)

class Box(Container):
	(HORIZONTAL,
	 VERTICAL) = [i for i in range(0, 2)]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.boxType = kwargs.get('type', Box.HORIZONTAL)

	def updateHorizonal(self):
		numWidgets = len(self.widgets)
		x, y, width, height = self.contentArea
		sectionSize = int(width / numWidgets)
		
		for i, widget in enumerate(self.widgets):
			area = x + i * sectionSize, y, sectionSize, height
			widget.assignArea(area)
			widget.update()

	def updateVertical(self):
		numWidgets = len(self.widgets)
		x, y, width, height = self.contentArea
		sectionSize = int(height / numWidgets)
		
		for i, widget in enumerate(self.widgets):
			area = x, y + i * sectionSize, width, sectionSize
			widget.assignArea(area)
			widget.update()

	def update(self):
		super().update()
		if not len(self.widgets):
			return

		""" update widget size and positions. """
		if self.boxType == Box.HORIZONTAL:
			self.updateHorizonal()
		elif self.boxType == Box.VERTICAL:
			self.updateVertical()
		

import pygame

from interface.widget import Widget

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

	""" Draw all the widgets in the Container. """
	def draw(self, surface):
		self.drawBorder(surface)
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

		self.borderColor = GREEN
		self.border = 1
		self.borderWidth = 1
	
	def update(self):
		super().update()
		for widget in self.widgets:
			widget.assignArea(self.rect)
			widget.update()

	def drawBorder(self, surface):
		if self.borderVisible:
			x, y, width, height = self.rect
			rect = x, y, width, height
			# outer border is easy to draw it is just the bounding rectangle.
			pygame.draw.rect(surface, self.borderColor, rect, self.border)
			# calculate inner border and draw it
			inner = x + self.borderWidth + self.border * 2, \
					y + self.borderWidth + self.border * 2, \
					width - (self.borderWidth + self.border * 2) * 2, \
					height - (self.borderWidth + self.border * 2) * 2
			pygame.draw.rect(surface, self.borderColor, inner, self.border, border_radius=10)

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
		x, y, width, height = self.rect
		sectionSize = int(width / numWidgets)
		
		for i, widget in enumerate(self.widgets):
			area = x + i * sectionSize, y, sectionSize, height
			widget.assignArea(area)
			widget.update()

	def updateVertical(self):
		numWidgets = len(self.widgets)
		x, y, width, height = self.rect
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
		

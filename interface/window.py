import os
import sys

import pygame

from interface.container import Container

from interface.colorDefs import *

pygame.init()
pygame.font.init()

moduleFilePath = os.path.abspath(sys.modules['__main__'].__file__)
projectRoot = os.path.dirname(moduleFilePath)

screenSize = screenWidth, screenHeight = 2560, 1350
screen = pygame.display.set_mode(screenSize)

fontName = "Roboto-Regular.ttf"
fontSize = 17

fontResourcePath = os.path.join(projectRoot, "resources/fonts")
fontPath = os.path.join(fontResourcePath, fontName)
print(f"{__name__} : loading font: {fontPath}")
UIFont = pygame.freetype.Font(fontPath, fontSize)

class App(Container):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.Running = True
		self.area = kwargs.get('area', (0, 0, *screenSize))

	def update(self):
		for widget in self.widgets:
			widget.assignArea(self.area)
			widget.update()

	def quitApplication(self):
		pygame.quit()
		quit()

	def run(self):
		""" update widgets once. """
		self.update()
		""" Run the main loop. """
		while self.Running:
			""" handle all the events. """
			for event in pygame.event.get():
				for widget in self.widgets:
					widget.handleEvents(event)
				""" Exit on pressing escape. """
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.Running = False
				""" Exit on hitting the window X. """
				if event.type == pygame.QUIT:
					self.Running = False
			""" process and draw all the events."""
			screen.fill(BLACK)
			self.processEvents()
			for widget in self.widgets:
				widget.processEvents()
				widget.draw(screen)
			pygame.display.flip()
		self.quitApplication()
from PyQt6.QtCore import QRect
from enemy import Enemy

class Beetle(Enemy):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


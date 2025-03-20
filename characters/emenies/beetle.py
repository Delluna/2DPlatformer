from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

from enemy import Enemy

class Beetle(Enemy):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)  


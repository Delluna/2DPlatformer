from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect 
from PyQt6.QtGui import QColor

from characters.obstacles.platform import Platform
from characters.emenies.enemy import Enemy
from scenes.scene import Scene

class TestScene(Scene):
    def __init__(self, width=800, height=600, ground_level=500):
        super().__init__(width=width, height=height, ground_level=ground_level)
        
        self.add_static_text(400, 300, "Hello!")
        
        # doors/adjacency scenes
        self.add_door(1, 0, 400)
        self.add_door(2, 799, 400)
    
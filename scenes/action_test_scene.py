from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect 
from PyQt6.QtGui import QColor

from scenes.scene import Scene
from characters.obstacles.platform import Platform

class ActionScene(Scene):
    '''
    该场景用于测试player的移动功能，包括：
    非跳跃时的左右移动、跳跃时的左右移动、二段跳、螳螂爪、遇到地面或墙体跳跃重置、冲刺、下蹲
    '''
    def __init__(self, width=800, height=600, ground_level=500):
        super().__init__(width=width, height=height, ground_level=ground_level)
        
        # obstacles
        self.obstacles.append(Platform(100, 80, 50, 380))
        self.obstacles.append(Platform(300, 80, 50, 380))
        self.obstacles.append(Platform(400, 400, 150, 50))
        self.obstacles.append(Platform(650, 250, 150, 50))
        
        # door/djacency scenes
        self.add_door(0, 799, 400)
        
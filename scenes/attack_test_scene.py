from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect 
from PyQt6.QtGui import QColor

from scenes.scene import Scene

from characters.obstacles.platform import Platform
from characters.emenies.beetle import Beetle

class AttackScene(Scene):
    '''
    该场景用于测试player的攻击功能
    场景中的敌人会自动复活，复活时间间隔为2000ms
    '''
    def __init__(self, width=800, height=600, ground_level=500):
        super().__init__(width=width, height=height, ground_level=ground_level)
        
        # obstacles
        self.obstacles.append(Platform(275, 300, 350, 50))
        
        # enemies
        self.enemies.append(Beetle(400, 250, 50, 50))
        self.enemies.append(Beetle(600, 450, 50, 50))
        
        for enemy in self.enemies:
            enemy.is_able_resurrect = True
            enemy.resurrection_time = 2000
        
        # door/adjacency scenes
        self.add_door(0, 0, 400)
   
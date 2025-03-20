from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect 
from PyQt6.QtGui import QColor

from characters.obstacles.platform import Platform
from characters.emenies.enemy import Enemy

class Scene:
    def __init__(self, width=800, height=600, ground_level=500):
        # background
        self.width = width
        self.height = height
        self.ground_level = ground_level
        
        # color
        self.background_color = QColor(135,206,235)
        self.ground_color = QColor(34, 139, 34)
        
        # obstacles
        self.obstacles = []
        
        # enemies
        self.enemies = []
        self.dead_enemies = []
    
    def draw(self, painter):
        
        # background
        painter.setBrush(self.background_color)  # 天空蓝色背景
        painter.drawRect(0, 0, self.width, self.height)  # 绘制矩形
        
        # ground
        painter.setBrush(self.ground_color)
        painter.drawRect(0, self.ground_level, self.width, self.height - self.ground_level)
        
        # obstacles
        for obstacle in self.obstacles:
            obstacle.draw(painter)
        
        # enemies
        for enemy in self.enemies:
            if not enemy.is_aliving:
                self.enemies.remove(enemy)
                if enemy.is_able_resurrect:
                    enemy.reset_aliving()
                    self.dead_enemies.append(enemy)
            enemy.draw(painter)
        
        for enemy in self.dead_enemies:
            if enemy.is_aliving:
                self.dead_enemies.remove(enemy)
                self.enemies.append(enemy)
        
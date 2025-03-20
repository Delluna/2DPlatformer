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
        
        # obstacles
        self.obstacles = []
        self.obstacles.append(Platform(300, 430, 150, 30))
        # self.obstacles.append(Platform(600, 350, 150, 30))
        self.obstacles.append(Platform(400, 100, 50, 230))
        
        # emenies
        self.enemies = []
        self.enemies.append(Enemy(600, 450, 50, 50))
    
    def draw(self, painter):
        
        # background
        painter.setBrush(QColor(135,206,235))  # 天空蓝色背景
        painter.drawRect(0, 0, self.width, self.height)  # 绘制矩形
        
        # ground
        painter.setBrush(QColor(34, 139, 34))
        painter.drawRect(0, self.ground_level, self.width, self.height - self.ground_level)
        
        # obstacles
        for obstacle in self.obstacles:
            obstacle.draw(painter)
        
        # enemies
        for enemy in self.enemies:
            if not enemy.is_aliving:
                self.enemies.remove(enemy)
                del enemy
                continue
            enemy.draw(painter)
        
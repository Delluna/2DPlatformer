from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

class Enemy:
    def __init__(self, x, y, width, height):
        self.hp = 1
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.is_aliving = True

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_aliving = False
        
    def draw(self, painter):
        print(self.hp)
        if self.is_aliving:
            painter.setBrush(QColor(79, 135, 34))
            painter.drawRect(self.get_enemy())
            
    def get_enemy(self):
        """返回敌人的矩形区域"""
        return QRect(self.x, self.y, self.width, self.height)

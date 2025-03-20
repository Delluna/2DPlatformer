# from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

class Door:
    """ 传送门 """
    def __init__(self, scene_id, x, y, width=1, height=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scene_id = scene_id  # 目标场景
    
    def draw(self, painter):
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.get_door())
        
    def get_door(self):
        return QRect(self.x, self.y, self.width, self.height)
        
        
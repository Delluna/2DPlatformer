from PyQt6.QtCore import QRect, QTimer
from PyQt6.QtGui import QColor

class Enemy(QRect):
    def __init__(self, x, y, width, height):
        # 正确调用基类的构造函数
        super().__init__(x, y, width, height)
        
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height

        self.color = QColor(0, 0, 0)
        self.hp = 1
        
        self.is_aliving = True
        self.is_able_resurrect = False
        self.resurrection_time = 2000  # 复活时间，单位ms

    def reset_aliving(self):
        if not self.is_aliving:
            QTimer.singleShot(self.resurrection_time, self._reset_aliving)
        
    def _reset_aliving(self):
        print('enemy resurrection')
        self.setX(self.default_x)
        self.setY(self.default_y)
        self.setWidth(self.default_width)
        self.setHeight(self.default_height)
        self.is_aliving = True
        
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_aliving = False
        
    def draw(self, painter):
        if self.is_aliving:
            painter.setBrush(QColor(79, 135, 34))
            painter.drawRect(self.get_enemy())
            
            
    def get_enemy(self):
        """返回敌人的矩形区域"""
        return QRect(self)

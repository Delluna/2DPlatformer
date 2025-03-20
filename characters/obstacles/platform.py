from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

    
class Platform(QRect):
    def __init__(self, x, y, width, height):
        # 正确调用基类的构造函数
        super().__init__(x, y, width, height)  

        self.color = QColor(0, 0, 0)

    def draw(self, painter):
        painter.setBrush(self.color)
        painter.drawRect(self.get_obstacle())
            
    def get_obstacle(self):
        return QRect(self)  # 直接返回自身
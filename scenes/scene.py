from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect 
from PyQt6.QtGui import QColor, QStaticText

from characters.obstacles.platform import Platform
from characters.emenies.enemy import Enemy
from characters.doors.door import Door

class Scene:
    def __init__(self, width=800, height=600, ground_level=500):
        # background
        self.width = width
        self.height = height
        self.ground_level = ground_level
        
        # color
        self.background_color = QColor(135,206,235)
        self.ground_color = QColor(34, 139, 34)
        
        # static texts
        self.static_texts = []
        
        # obstacles
        self.obstacles = []
        
        # enemies
        self.enemies = []
        self.dead_enemies = []
        
        # doors/adjacency scenes
        self.doors = []
    
    def add_static_text(self, x, y, text):
        static_text = [x, y, QStaticText(f"{text}")]
        self.static_texts.append(static_text)
        
    def add_door(self, scene_id, x, y, width=1, height=100):
        door = Door(scene_id, x, y, width, height)
        self.doors.append(door)
        
    def draw(self, painter):
        '''
        一定要按顺序放置，会有底到顶渲染，否则可能显示不出来
        '''
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
        
        # adjacency scenes
        for door in self.doors:
            door.draw(painter)
            
        # static texts
        painter.setBrush(QColor(0, 0, 0))
        for static_text in self.static_texts:
            painter.drawStaticText(static_text[0], static_text[1], static_text[2])
        
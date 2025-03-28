import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QColor, QStaticText

from characters.player import Player
from scenes.test_scene import TestScene
# from scenes.action_test_scene import ActionScene
# from scenes.attack_test_scene import AttackScene

from scenes.hash_scenes import create_scene

import global_arguments

class Main_Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        # 玩家状态
        self.player = Player(y=self.height())  # y=self.height()表示直接让玩家出现在地面上，否则玩家将从天上掉下来
        
        # 场景
        self.ground_level = 500
        self.current_scene = create_scene(0, self.width(), self.height(), self.ground_level)
        
        # 定时器，用来刷新游戏画面
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)  # 绑定更新函数  定时器每次出发时会调用self.update_game方法      
        self.timer.start(16)  # 约 60 FPS    表示每 16 ms 触发一次
    
    def initUI(self):
        self.setWindowTitle('2DPlatformer')
        self.setGeometry(100, 100, global_arguments.window_width, global_arguments.window_height)  # 设置窗口大小
        self.show()
        
    def keyPressEvent(self, event):
        if event.key() == global_arguments.key_move_left:
            global_arguments.left_pressed = True
        if event.key() == global_arguments.key_move_right:
            global_arguments.right_pressed = True
        if event.key() == global_arguments.key_move_crouch:
            global_arguments.down_pressed = True
        if not global_arguments.rush_pressed and event.key() == global_arguments.key_move_rush:
            global_arguments.rush_pressed = True
            self.player.rush()  # 冲刺
        if not global_arguments.jump_pressed and event.key() == global_arguments.key_move_jump:
            global_arguments.jump_pressed = True
            self.player.jump()  # 跳跃
        if not global_arguments.attack_pressed and event.key() == global_arguments.key_attack_normal:
            global_arguments.attack_pressed = True
            self.player.attack(enemies=self.current_scene.enemies)  # 攻击
        
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():  # 如果是自动重复，不处理，否则长按跳跃键会连续跳跃
            return  
        if event.key() == global_arguments.key_move_left:
            global_arguments.left_pressed = False
        if event.key() == global_arguments.key_move_right:
            global_arguments.right_pressed = False
        if event.key() == global_arguments.key_move_rush:
            global_arguments.rush_pressed = False
        if event.key() == global_arguments.key_move_crouch:
            global_arguments.down_pressed = False
        if event.key() == global_arguments.key_move_jump:
            global_arguments.jump_pressed = False
        if event.key() == global_arguments.key_attack_normal:
            global_arguments.attack_pressed = False
    
    def change_scene(self):
        """ 检测玩家是否进入门 """
        player_rect = self.player.get_player()
        for door in self.current_scene.doors:
            if player_rect.intersected(door.get_door()):
                self.current_scene = create_scene(door.scene_id, self.width(), self.height(), self.ground_level)
                if self.player.direction == 0:
                    self.player.set_position(x=self.width() - self.player.x - self.player.reset_position_interval,y=self.player.y)
                elif self.player.direction == 1:
                    self.player.set_position(x=self.player.default_x+self.player.reset_position_interval,y=self.player.y)
            
    
    def update_game(self):
        self.change_scene()  # 检测角色是否进入门，如果进入门，则需要场景切换
        self.player.update_c(obstacles=self.current_scene.obstacles)  # 下蹲运动
        self.player.update_x(0, self.width(), obstacles=self.current_scene.obstacles, enemies=self.current_scene.enemies)  # 水平运动
        self.player.update_y(0, self.current_scene.ground_level, obstacles=self.current_scene.obstacles, enemies=self.current_scene.enemies)  # 垂直运动
        self.player.update_img()
        self.update()  # 刷新窗口， self.update()方法会触发paintEvent()重新绘制窗口
    
    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 开启抗锯齿渲染技术
            
            # 绘制地图
            self.current_scene.draw(painter)
            
            # 玩家
            self.player.draw(painter)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Main_Window()
    sys.exit(app.exec())
            

import os
from collections import deque
from PyQt6.QtCore import QRect, QTimer
from PyQt6.QtGui import QColor, QStaticText, QImage, QPen

import global_arguments
from utils.utils import is_horizontal_adjacent

class Player:
    def __init__(self, hp=3, mp=3, x=10, y=0, width=50, height=50, velocity_x=5, velocity_y=0, gravity=1, jump_strength=-15, rush_scale = 3):
        # 默认值
        self.default_hp = hp
        self.default_mp = mp
        self.default_x = x
        self.default_y = y
        self.default_width = width
        self.default_height = height
        self.default_velocity_x = velocity_x  # 默认水平速度
        self.default_velocity_y = velocity_y  # 默认垂直速度
        self.default_gravity = gravity  # 默认重力
        
        # 当前状态
        self.hp = self.default_hp
        self.mp = self.default_mp
        self.x = self.default_x
        self.y = self.default_y
        self.width = self.default_width
        self.height = self.default_height
        self.color = QColor(255, 0, 0)
        self.direction = 1  # 人物朝向，0:'left', 1:'right', 2:'up', 3:'down'
        self.velocity_x = self.default_velocity_x  # 水平速度
        self.velocity_y = self.default_velocity_y  # 垂直速度
        self.gravity = self.default_gravity  # 重力
        
        # self.state = {
        #     'is_aliving': True,
        #     'is_jumping': False,
        #     'is_second_jumping': False,
        #     'is_crouching' : False,
        #     'is_attacking' : False,
        #     'is_walling': False,
        # }
        
        self.is_aliving = True
        self.is_jumping = False
        self.is_second_jumping = False
        self.is_crouching = False  # 下蹲
        self.is_attacking = False
        self.is_walling = False
        
        # 攻击能力
        self.normal_attack_damage = 1  # 攻击伤害
        self.normal_attack_duration = 200  # 攻击持续时间，单位ms
        self.normal_attack_cooldown = False  # 攻击冷却
        self.normal_attack_cooldown_time = 0  # 攻击冷却时间，单位ms
        self.normal_attack_range = {'width': 40, 'height': 40}  # 攻击空间
        self.normal_attack_box = None
        
        # 跳跃能力
        self.jumping_ability = True  # 跳跃能力
        self.jump_strength = jump_strength  # 垂直速度
        self.second_jumping_ability = True  # 二段跳能力
        self.claw_jumping_ability = True  # 螳螂爪能力
        
        # 冲刺能力
        self.rush_ability = True  # 冲刺能力
        self.rush_strength = rush_scale * velocity_x  # 冲刺
        self.rush_duration = 200  # 冲刺持续时间，单位ms
        
        self.reset_position_interval = self.width
        
        # 图片
        self.default_player_img_path = os.path.join(global_arguments.animations_player_root, 'walkStart', '0.png')
        self.walk_index = 0
        self.player_img = QImage(self.default_player_img_path)
        
        self.imgs_path = deque()
         
    def reset_jumping(self):
        self.is_jumping = False
        self.is_second_jumping = False
    
    def reset_normal_attack_cooldown(self):
        self.normal_attack_cooldown = False
    
    def reset_velocity_x(self):
        self.set_velocity_x(self.default_velocity_x)
    
    def reset_position(self):
        self.set_position(self.default_x, self.default_y)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_gravity(self, gravity):
        self.gravity = gravity
        
    def set_velocity_x(self, velocity_x):
        self.velocity_x = velocity_x
        
    def set_velocity_y(self, velocity_y):
        self.velocity_y = velocity_y
    
    def set_direction(self, direction):
        self.direction = direction
        
    def move_left(self):
        self.x -= self.velocity_x
    
    def move_right(self):
        self.x += self.velocity_x
        
    def load_imgs(self, action):
        root = os.path.join(global_arguments.animations_player_root, action)
        for _, _, imgs in os.walk(root):
            for img in reversed(imgs):
                self.imgs_path.append(os.path.join(root, img))
            
    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            # self.is_aliving = False
            # self.hp = 0
            
            print('玩家复活')
            self.hp = self.default_hp
            self.reset_position()
        
    def crouch(self):
        self.y += self.height // 2
        self.height = self.height // 2
        
    def stretch(self):
        self.y -= self.height
        self.height *= 2
    
    def rush(self):
        if self.rush_ability:
            self.velocity_x = self.rush_strength
            self.set_gravity(self.default_gravity)
            self.is_walling = False
            # 冲刺动画
            QTimer.singleShot(0, lambda: self.load_imgs('rush'))
            QTimer.singleShot(self.rush_duration, self.reset_velocity_x)
        
    def jump(self):
        # 二段跳
        if self.jumping_ability and self.second_jumping_ability and self.is_jumping and not self.is_second_jumping:
            self.set_velocity_y(self.jump_strength)
            self.set_gravity(self.default_gravity)
            self.is_second_jumping = True
            self.is_walling = False
            # 跳跃动画
            QTimer.singleShot(0, lambda: self.load_imgs('jump'))
            
        # 跳跃
        if self.jumping_ability and not self.is_jumping:
            self.set_velocity_y(self.jump_strength)
            self.set_gravity(self.default_gravity)
            self.is_jumping = True
            self.is_walling = False
            # 跳跃动画
            QTimer.singleShot(0, lambda: self.load_imgs('jump'))
        
    def attack(self, enemies=None):
        if self.normal_attack_cooldown:
            return
        self.is_attacking = True
        self.normal_attack_cooldown = True
        
        # 计算攻击区域
        if self.direction == 0:
            self.normal_attack_box = QRect(self.x - self.normal_attack_range['width'], 
                               self.y + self.height // 2 - self.normal_attack_range['height'] // 2, 
                               self.normal_attack_range['width'],
                               self.normal_attack_range['height'])
        if self.direction == 1:
            self.normal_attack_box = QRect(self.x + self.width, 
                               self.y + self.height // 2 - self.normal_attack_range['height'] // 2, 
                               self.normal_attack_range['width'],
                               self.normal_attack_range['height'])
        
        # 攻击碰撞检测
        if enemies:
            for enemy in enemies:
                if enemy.is_aliving and self.normal_attack_box.intersects(enemy.get_enemy()):
                    enemy.take_damage(self.normal_attack_damage)
        
        QTimer.singleShot(0, lambda: self.load_imgs('attack_0'))
        QTimer.singleShot(self.normal_attack_duration, self.end_attack)        # QTimer.singleShot(延迟时间, 需要执行的函数)，用于在 指定时间后执行某个函数（不需要括号），但不会重复执行。
        QTimer.singleShot(self.normal_attack_cooldown_time, self.reset_normal_attack_cooldown)
    
    def end_attack(self):
        self.is_attacking = False
        self.normal_attack_box = None
        
    def defense(self):
        pass
    
    def update_c(self, obstacles=None):
        # 下蹲
        if global_arguments.down_pressed and not self.is_crouching:
            self.crouch()
            self.is_crouching = True
        
        # 站起
        if not global_arguments.down_pressed and self.is_crouching:
            self.stretch()
            # 如果头顶障碍物，导致站起所需空间不足，则不站起
            player_rect = self.get_player()
            flag = any(player_rect.intersected(obstacle) for obstacle in obstacles)
            if not flag:
                self.is_crouching = False
                return
            else:
                self.crouch()
            
    
    def update_x(self, border_left, border_right, obstacles=None, enemies=None):
        # 左移
        if global_arguments.left_pressed:
            self.move_left()
            self.set_direction(0)
        
        # 屏幕边界
        if self.x < border_left:
            self.x = border_left
            # if self.claw_jumping_ability:
            #     self.reset_jumping()
                
        # 障碍物
        player_rect = self.get_player()
        for obstacle in obstacles: 
            if player_rect.intersected(obstacle) and player_rect.x() <= obstacle.x() + obstacle.width():
                self.x = obstacle.x() + obstacle.width()
                if self.claw_jumping_ability:
                    self.reset_jumping()  
        
        # 敌人
        player_rect = self.get_player()
        for enemy in enemies:
            if enemy.is_aliving and player_rect.intersected(enemy) and player_rect.x() <= enemy.x() + enemy.width():
                self.x = enemy.x() + enemy.width() + self.reset_position_interval
                self.take_damage()
            
        # 右移        
        if global_arguments.right_pressed:
            self.move_right()
            self.set_direction(1)
            
        # 屏幕边界
        if self.x > border_right - self.width:
            self.x = border_right - self.width
            # if self.claw_jumping_ability:
            #     self.reset_jumping()
            
        # 障碍物   
        player_rect = self.get_player()
        for obstacle in obstacles:
            if player_rect.intersected(obstacle) and player_rect.x() >= obstacle.x() - player_rect.width():
                self.x = obstacle.x() - player_rect.width()
                if self.claw_jumping_ability:
                    self.reset_jumping() 
        
        # 敌人
        player_rect = self.get_player()
        for enemy in enemies:
            if enemy.is_aliving and player_rect.intersected(enemy) and player_rect.x() >= enemy.x() - player_rect.width():
                self.x = enemy.x() - player_rect.width() - self.reset_position_interval
                self.take_damage()
                                  
            
    def update_y(self, ceiling_level, ground_level, obstacles=None, enemies=None):
        # 垂直位置变化
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # 上升过程
        # 天花板
        if self.y < ceiling_level:
            self.y = ceiling_level
            self.velocity_y = 0
            
        # 障碍物
        player_rect = self.get_player()
        for obstacle in obstacles:
            # 不能超过平台
            if player_rect.intersected(obstacle) and self.velocity_y < 0:
                self.y = obstacle.y() + obstacle.height()
                self.velocity_y = 0
        
        # 敌人
        player_rect = self.get_player()
        for enemy in enemies:
            if enemy.is_aliving and player_rect.intersected(enemy) and self.velocity_y < 0:
                self.y = enemy.y() + enemy.height() + self.reset_position_interval
                self.take_damage()
            
        # 下降过程
        # 地面
        if self.y > ground_level - self.height:
            self.y = ground_level - self.height
            self.velocity_y = 0
            self.reset_jumping()
        
        # 障碍物
        player_rect = self.get_player()
        for obstacle in obstacles:
            # 站在平台上 
            if player_rect.intersected(obstacle) and self.velocity_y > 0:
                self.y = obstacle.y() - self.height
                self.velocity_y = 0
                self.reset_jumping()
            # 螳螂爪
            if self.claw_jumping_ability and self.velocity_y > 0:
                if is_horizontal_adjacent(player_rect, obstacle) and (global_arguments.left_pressed or global_arguments.right_pressed):  # 匀速下滑
                    self.set_gravity(0)
                    self.set_velocity_y(1)
                    self.is_walling = obstacle
                    self.imgs_path.append(os.path.join(global_arguments.animations_player_root, 'Wall.png'))
                elif self.is_walling == obstacle and ((obstacle.left() < self.x and  not global_arguments.left_pressed) or (obstacle.right() > self.x and not global_arguments.right_pressed)):
                    self.set_gravity(self.default_gravity)
                    self.is_walling = False
                        
        # 敌人
        # player_rect = self.get_player()
        # for enemy in enemies:
        #     if enemy.is_aliving and player_rect.intersected(enemy) and self.velocity_y > 0:
        #         ??
        #         self.hp -= 1
        #         self.take_damage()
    
    def update_img(self):
        # 左右移动
        if global_arguments.left_pressed or global_arguments.right_pressed:
            self.imgs_path.appendleft(os.path.join(global_arguments.animations_player_root, 'walk', str(self.walk_index) + '.png'))
            self.walk_index = (self.walk_index + 1) % 8
        else:
            self.imgs_path = deque([img_path for img_path in self.imgs_path if img_path.split('\\')[-2] != 'walk'])
        
        # 加载图片
        if self.imgs_path:
            self.player_img_path = self.imgs_path.pop()
        else:
            self.player_img_path = self.default_player_img_path
        
        self.player_img = QImage(self.player_img_path)
        print(self.is_walling)
        
        # 反转图片
        if self.direction == 0:
            self.player_img = self.player_img.mirrored(horizontal=True,vertical=False)
        if self.is_walling != False:
            self.player_img = self.player_img.mirrored(horizontal=True,vertical=False)
        
    
    def draw(self, painter):
        painter.drawStaticText(10, 10, QStaticText(f"HP: {self.hp}"))
        
        if self.is_aliving:
            painter.setPen(QColor(0, 0, 0, 0))  # 边框透明
            painter.setBrush(QColor(0, 0, 0, 0))  # 填充透明
            painter.drawRect(self.get_player())
            painter.drawImage(self.get_player(), self.player_img)
        
            # 攻击效果渲染
            # if self.normal_attack_box:
            #     painter.setBrush(QColor(0, 255, 0))
            #     painter.drawRect(self.normal_attack_box)
    
    def get_player(self):
        return QRect(self.x, self.y, self.width, self.height)
    

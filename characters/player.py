from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

import global_arguments
from utils.utils import is_horizontal_adjacent

class Player:
    def __init__(self, hp=3, mp=3, x=0, y=0, width=50, height=50, velocity_x=5, velocity_y=0, gravity=1, jump_strength=-15, sprint_scale = 3):
        self.hp = hp
        self.mp = mp
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # 默认值
        self.default_velocity_x = velocity_x  # 默认水平速度
        self.default_velocity_y = velocity_y  # 默认垂直速度
        self.default_gravity = gravity  # 默认重力
        
        # 当前值
        self.velocity_x = self.default_velocity_x  # 水平速度
        self.velocity_y = self.default_velocity_y  # 垂直速度
        
        self.gravity = self.default_gravity  # 重力
        self.jump_strength = jump_strength  # 垂直加速度
        self.sprint_strength = sprint_scale * velocity_x  # 冲刺能力
        self.is_jumping = False
        self.is_second_jumping = False
        self.is_crouching = False  # 下蹲
        
        self.jumping_ability = True  # 跳跃能力
        self.second_jumping_ability = True  # 二段跳能力
        self.claw_jumping_ability = True  # 螳螂爪能力
        self.sprint_ability = True  # 冲刺能力
        
        self.color = QColor(255, 0, 0)
    
    def move_left(self):
        self.x -= self.velocity_x
    
    def move_right(self):
        self.x += self.velocity_x

    def sprint_left(self):
        self.x -= self.sprint_strength
    
    def sprint_right(self):
        self.x += self.sprint_strength
        
    def crouch(self):
        self.y += self.height // 2
        self.height /= 2
        
    def stretch(self):
        self.y -= self.height
        self.height *= 2
    
    def jump(self):
        # 二段跳
        if self.jumping_ability and self.second_jumping_ability and self.is_jumping and not self.is_second_jumping:
            self.set_velocity_y(self.jump_strength)
            self.set_gravity(self.default_gravity)
            self.is_second_jumping = True
            
        # 跳跃
        if self.jumping_ability and not self.is_jumping:
            self.set_velocity_y(self.jump_strength)
            self.set_gravity(self.default_gravity)
            self.is_jumping = True
    
    def reset_jumping(self):
        self.is_jumping = False
        self.is_second_jumping = False
    
    def set_gravity(self, gravity):
        self.gravity = gravity
        
    def set_velocity_y(self, velocity_y):
        self.velocity_y = velocity_y
        
    def attack(self):
        pass
    
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
            if obstacles:
                player_rect = self.get_player()
                flag = any(player_rect.intersected(obstacle) for obstacle in obstacles)
                if not flag:
                    self.is_crouching = False
                    return
                else:
                    self.crouch()
            
    
    def update_x(self, border_left, border_right, obstacles=None):
        # 左移
        if global_arguments.left_pressed:
            if self.sprint_ability and global_arguments.sprint_pressed:
                self.sprint_left()
            else:
                self.move_left()
        
        # 屏幕边界
        if self.x < border_left:
            self.x = border_left
            # if self.claw_jumping_ability:
            #     self.reset_jumping()
                
        # 障碍物
        if obstacles:
            player_rect = self.get_player()
            for obstacle in obstacles: 
                if player_rect.intersected(obstacle) and player_rect.x() <= obstacle.x() + obstacle.width():
                    self.x = obstacle.x() + obstacle.width()
                    if self.claw_jumping_ability:
                        self.reset_jumping()  
            
        # 右移        
        if global_arguments.right_pressed:
            if self.sprint_ability and global_arguments.sprint_pressed:
                self.sprint_right()
            else:
                self.move_right()
            
        # 屏幕边界
        if self.x > border_right - self.width:
            self.x = border_right - self.width
            # if self.claw_jumping_ability:
            #     self.reset_jumping()
            
        # 障碍物   
        if obstacles:
            player_rect = self.get_player()
            for obstacle in obstacles:
                if player_rect.intersected(obstacle) and player_rect.x() >= obstacle.x() - player_rect.width():
                    self.x = obstacle.x() - player_rect.width()
                    if self.claw_jumping_ability:
                        self.reset_jumping() 
                                  
            
    def update_y(self, ceiling_level, ground_level, obstacles=None):
        # 垂直位置变化
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # 上升过程
        # 天花板
        if self.y < ceiling_level:
            self.y = ceiling_level
            self.velocity_y = 0
            
        # 障碍物
        if obstacles:
            player_rect = self.get_player()
            for obstacle in obstacles:
                # 不能超过平台
                if player_rect.intersected(obstacle) and self.velocity_y < 0:
                    self.y = obstacle.y() + obstacle.height()
                    self.velocity_y = 0
            
        # 下降过程
        # 地面
        if self.y > ground_level - self.height:
            self.y = ground_level - self.height
            self.velocity_y = 0
            self.reset_jumping()
        
        # 障碍物
        if obstacles:
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
                    else:
                        self.set_gravity(self.default_gravity)
    
    def get_player(self):
        return QRect(self.x, self.y, self.width, self.height)
    
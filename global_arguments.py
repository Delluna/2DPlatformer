from PyQt6 import QtCore

animations_player_root = 'assets\\animations\\player'


# 按键绑定
key_move_left = QtCore.Qt.Key.Key_A
key_move_right = QtCore.Qt.Key.Key_D
key_move_rush = QtCore.Qt.Key.Key_Shift
key_move_crouch = QtCore.Qt.Key.Key_S
key_attack_normal = QtCore.Qt.Key.Key_J
key_move_jump = QtCore.Qt.Key.Key_K


window_width = 800
window_height = 600

left_pressed = False
right_pressed = False
rush_pressed = False
down_pressed = False
jump_pressed = False
attack_pressed = False

from PyQt6 import QtCore

# 按键绑定
move_left = QtCore.Qt.Key.Key_A
move_right = QtCore.Qt.Key.Key_D
move_sprint = QtCore.Qt.Key.Key_Shift
move_crouch = QtCore.Qt.Key.Key_S
move_jump = QtCore.Qt.Key.Key_K


window_width = 800
window_height = 600

left_pressed = False
right_pressed = False
sprint_pressed = False
down_pressed = False
jump_pressed = False

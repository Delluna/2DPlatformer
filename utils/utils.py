from PyQt6.QtCore import QRect

def is_horizontal_adjacent(rect1: QRect, rect2: QRect) -> bool:
    if rect1.intersects(rect2):
        return False  # 如果相交，则不是相邻

    # 检查是否水平相邻
    horizontal_adjacent = (
        rect1.right() + 1 == rect2.left() or rect2.right() + 1 == rect1.left()
    ) and (rect1.top() <= rect2.bottom() and rect1.bottom() >= rect2.top())

    return horizontal_adjacent
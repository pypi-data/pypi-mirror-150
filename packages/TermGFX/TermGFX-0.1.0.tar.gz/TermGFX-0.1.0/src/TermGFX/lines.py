from engine import Canvas
from shapes import Line


window_size = (20, 22)

canvas = Canvas(window_size)

line = Line((0, 0), (2, 1), "█", algorithm="bresenham")

line.draw(canvas)

canvas.draw()
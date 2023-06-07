from libqtile.widget import base
from libqtile import bar

import math
import cairocffi as cairo


class Border(base._Widget):

    SHAPES = [
        "semicricle",
        "triangle"
    ]

    def __init__(self, side, shape, foreground=None, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.side = side if side in ["left", "right"] else "left"
        self.shape = shape
        self.foreground = foreground if foreground else "ffffff"

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)

    def calculate_length(self):
        if self.bar.horizontal:
            return self.bar.height / 2
        else:
            return 0

    def draw(self):

        self.drawer.clear(self.bar.background)
        self.drawer.set_source_rgb(self.foreground)

        if self.shape == "triangle":
            y = [self.bar.height / 2, 0, self.bar.height]
            if self.side == "left":
                x = [self.length * 0.2, self.length, self.length]
            else:
                x = [self.length * 0.8, 0, 0]
            self._draw_triangle(x, y)

        elif self.shape == "semicricle":
            y = self.bar.height / 2
            if self.side == "left":
                x = self.length
            else:
                x = 0
            self._draw_circle(
                x,
                y,
                self.bar.height / 2,
                0,
                math.pi * 2
            ) 

        self.drawer.draw(
            offsetx=self.offset,
            offsety=self.offsety,
            width=self.length
        )

    def _draw_triangle(self, x: list, y: list):
        self.drawer.ctx.new_sub_path()
        self.drawer.ctx.move_to(x[0], y[0])
        self.drawer.ctx.line_to(x[1], y[1])
        self.drawer.ctx.line_to(x[2], y[2])
        self.drawer.ctx.fill()

    def _draw_circle(self, x, y, radius, angle1, angle2):
        self.drawer.ctx.new_sub_path()
        self.drawer.ctx.arc(x, y, radius, angle1, angle2) 
        self.drawer.ctx.fill()

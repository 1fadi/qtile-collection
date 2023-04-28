from libqtile.widget import base
from libqtile.log_utils import logger
from libqtile import bar

import math
import cairocffi as cairo
import subprocess
import re


class Volume(base._Widget):
    """A widget to display a dynamic volume icon.
    uses "amixer sget" command to get the volume level.
    """ 

    defaults = [
        ("padding", 4, "padding"),
        ("update_interval", 0.2, "update status in seconds."),
        ("size", 20, "size of the widget."),
        ("foreground", "ffffff", "widget's foreground"),
        ("background", None, "widget's background"),
        ("channel", "Master", "channel"),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(Volume.defaults)
        self.margin = 2
        self.WIDTH = self.size
        self.HEIGHT = self.calc_height()
        self.widget_width = self.WIDTH + self.margin * 2
        self.length = self.padding * 2 + self.widget_width

    def get_volume(self, channel):
        output = subprocess.getoutput(f"amixer sget {channel}")
        re_vol = re.compile(r"(\d?\d?\d?)%")
        re_mute = re.compile(r"(\[on\]|\[off\])")
        
        results = re_vol.search(output)
        if results is None:
            logger.exception("Error: couldn't get volume level.")
            return 0, ""
        else:
            vol = int(re_vol.search(output).groups()[0])
            return vol, re_mute.search(output).groups()[0]

    def calculate_length(self):
        if self.bar.horizontal:
            return (self.padding * 2) + self.widget_width
        else:
            return 0

    def draw(self):
        vol, status = self.get_volume(self.channel)
        self.draw_icon(vol, status)

    def draw_icon(self, vol, status):
        y_margin = (self.bar.height - self.HEIGHT) / 2
        mp = self.margin + self.padding

        self.drawer.clear(self.background or self.bar.background)
        self.drawer.set_source_rgb(
            self.foreground if self.foreground else "ffffff"
        )
        self._draw_rect(
            mp,
            y_margin,
            self.WIDTH / 3,
            self.HEIGHT,
            1,
            0.8
        )
        x1, y1 = mp + (self.WIDTH / 3) / 3, self.bar.height / 2
        x2, y2 = mp + (self.WIDTH / 3) + (self.WIDTH / 3) / 2, y1 - self.HEIGHT
        x3, y3 = x2, y1 + self.HEIGHT

        self.drawer.ctx.new_sub_path()
        self.drawer.ctx.set_operator(cairo.OPERATOR_SOURCE)
        self.drawer.ctx.move_to(x1, y1)
        self.drawer.ctx.line_to(x2, y2)
        self.drawer.ctx.line_to(x3, y3)
        self.drawer.ctx.close_path()
        self.drawer.ctx.fill()

        center = x1 + (self.WIDTH / 3)
        self.drawer.ctx.set_line_width(1)
        if 0 < vol <= 33 or vol > 33:
            self.drawer.ctx.new_sub_path()
            self.drawer.ctx.arc(
                center,
                self.bar.height / 2,
                ((self.WIDTH + mp) - center) * 0.4,
                -math.pi / 4,
                math.pi /4,
            )
        if 33 < vol <= 66 or vol > 66:
            self.drawer.ctx.new_sub_path()
            self.drawer.ctx.arc(
                center,
                self.bar.height / 2,
                ((self.WIDTH + mp) - center) * 0.6,
                -math.pi / 3,
                math.pi / 3,
            )
        if 66 < vol <= 100:
            self.drawer.ctx.new_sub_path()
            self.drawer.ctx.arc(
                center,
                self.bar.height /2,
                ((self.WIDTH + mp) - center) * 0.8,
                -math.pi / 2.5,
                math.pi /2.5,
            )
        self.drawer.ctx.stroke()

        if status == "[off]":
            self.drawer.ctx.set_line_width(1)
            self.drawer.set_source_rgb("000000")
            self.drawer.ctx.move_to(mp + self.WIDTH, y2)
            self.drawer.ctx.line_to(mp, y3)
            self.drawer.ctx.stroke()

            self.drawer.ctx.set_line_width(2)
            self.drawer.set_source_rgb(self.foreground)
            self.drawer.ctx.move_to(mp + self.WIDTH, y2  + 1)
            self.drawer.ctx.line_to(mp, y3 + 1)
            self.drawer.ctx.stroke()

            self.drawer.ctx.set_line_width(1)
            self.drawer.set_source_rgb("000000")
            self.drawer.ctx.move_to(mp + self.WIDTH, y2 + 2)
            self.drawer.ctx.line_to(mp, y3 + 2)
            self.drawer.ctx.stroke()

        self.drawer.draw(
            offsetx=self.offset,
            offsety=self.offsety,
            width=self.length
        )

    def calc_height(self):
        actual_width = (self.WIDTH + self.margin + self.padding)
        width_33 = self.WIDTH / 3
        x_44 = self.margin + self.padding + width_33 + width_33 / 3
        return (actual_width - x_44) * 0.8

    def _draw_rect(self, x, y, width, height, linewidth, aspect):
        aspect = aspect
        corner_radius = height / 5.0
        radius = corner_radius / aspect
        degrees = math.pi / 180.0

        self.drawer.ctx.new_sub_path()

        delta = radius + linewidth / 2
        self.drawer.ctx.arc(
            x + width - delta,
            y + delta,
            radius,
            -90 * degrees,
            0 * degrees
        )
        self.drawer.ctx.arc(
            x + width - delta,
            y + height - delta,
            radius,
            0 * degrees,
            90 * degrees
        )
        self.drawer.ctx.arc(
            x + delta,
            y + height - delta,
            radius,
            90 * degrees,
            180 * degrees
        )
        self.drawer.ctx.arc(
            x + delta,
            y + delta,
            radius,
            180 * degrees,
            270 * degrees
        )
        self.drawer.ctx.close_path()
        self.drawer.ctx.fill()

    def timer_setup(self):
        self.draw()
        if self.update_interval is not None:
            self.timeout_add(self.update_interval, self.timer_setup)

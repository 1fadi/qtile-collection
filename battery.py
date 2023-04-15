from libqtile.widget import base
from libqtile.log_utils import logger
import math
import cairocffi as cairo

from utils import bat


class Battery(base._Widget):
    """A widget to display battery."""

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("padding", 4, ""),
        ("foreground", "ffffff", "Battery color in normal mode."),
        ("charging_fg", "02a724", "foreground color when battery is charging."),
        ("update_interval", 30, "time to wait until the widgets refreshes."),
        ("low_foreground", "ff0000", "change color when battery is low."),
        ("warn_below", 10, "battery level to indicate battery is low."),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, 1, **config)
        self.add_defaults(Battery.defaults)
        self.linewidth = 36
        self.length = self.padding * 2 + self.linewidth
        self.HEIGHT = 16

    def draw(self):
        percent, charging = self.get_bat()
        if charging:
            self.foreground = self.charging_fg
        elif percent <= self.warn_below:
            self.foreground = self.low_foreground
        self.draw_battery(percent)

    def draw_battery(self, percent):
        self.drawer.clear(self.background or self.bar.background)
        if self.bar.horizontal:
            PERCENT = 30 / 100 * percent
            y_margin = (self.bar.height - self.HEIGHT) / 2

            self.drawer.set_source_rgb("8c8c8c")
            self._fill_body(
                1,
                y_margin,
                width=30,
                height=self.HEIGHT,
                linewidth=1
            )
            self.drawer.set_source_rgb(self.foreground)
            self._border(
                1,
                y_margin,
                width=30,
                height=self.HEIGHT,
                linewidth=2.6
            )
            if percent <= self.warn_below:
                self.drawer.set_source_rgb(self.low_foreground)
            else:
                self.drawer.set_source_rgb("ff8c1a")
            self._fill_body(
                2,
                y_margin,
                width=PERCENT,
                height=self.HEIGHT,
                linewidth=1
            )
            self.drawer.set_source_rgb("000000")
            self._border(
                1,
                y_margin,
                width=30,
                height=self.HEIGHT,
                linewidth=0.6
            )
            self.drawer.set_source_rgb(self.foreground)
            self._fill_body(
                28,
                y_margin + 1,
                width=8.3,
                height=self.HEIGHT -2,
                linewidth=5
            )
            self.drawer.ctx.select_font_face("sans",cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            self.drawer.ctx.set_font_size(12)
            self.drawer.ctx.move_to(4, self.HEIGHT)
            self.drawer.set_source_rgb("ffffff")
            self.drawer.ctx.show_text(str(percent))

            self.drawer.draw(
                offsetx=self.offset + self.padding, offsety=self.offsety, width=self.length
            )

    def get_bat(self):
        return bat()

    def _rounded_body(self, x, y, width, height, linewidth):
        y_margin = (self.bar.height - height) / 2
        aspect = 1.0
        corner_radius = height / 4.0
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

    def _border(self, x, y, width, height, linewidth):
        self._rounded_body(x, y, width, height, linewidth)
        self.drawer.ctx.set_line_width(linewidth)
        self.drawer.ctx.stroke()

    def _fill_body(self, x, y, width, height, linewidth):
        self._rounded_body(x, y, width, height, linewidth)
        self.drawer.ctx.fill()

    def timer_setup(self):
        def on_done(future):
            try:
                result = future.result()
            except Exception:
                result = None
                logger.exception("line 154")

            if result is not None:
                try:
                    self.update(result)

                    if self.update_interval is not None:
                        self.timeout_add(self.update_interval, self.timer_setup)

                except Exception:
                    logger.exception("Failed to reschedule.")

        self.future = self.qtile.run_in_executor(self.draw)
        self.future.add_done_callback(on_done)

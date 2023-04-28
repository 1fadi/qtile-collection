from libqtile.widget import base
from libqtile.log_utils import logger
from libqtile import bar

import math
import cairocffi as cairo
import netifaces
import socket


class Network(base._Widget):
    """A simple widget to indicate network connection.
    required param: interfaces -> list

    requirements: netifaces
    """

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("interfaces", [], "Network interfaces."),
        ("padding", 4, "padding on either side of of the widget."),
        ("foreground", "d5d5d5", "Widget's foreground."),
        ("update_interval", 2, "time to wait until the widgets refreshes."),
        ("size", 14, "Size of the widget."),
    ]

    def __init__(self, interfaces, **config):
        base._Widget.__init__(self, bar.CALCULATED, **config)
        self.add_defaults(Network.defaults)
        self.interfaces = interfaces
        self.HEIGHT = self.WIDTH = self.size
        self.margin = 2
        self._foreground = self.foreground if self.foreground else "d5d5d5"

    def calculate_length(self):
        if self.bar.horizontal:
            return (self.padding * 2) + self.WIDTH + self.margin * 2
        else:
            return 0

    def parse_connection(self):
        
        def ping():
            """checks if there is a connection"""
            try:
                socket.setdefaulttimeout(1)
                socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = "1.1.1.1"
                port = 80
                server_addr = (host, port)
                socket_obj.connect(server_addr)
            except OSError:
                return False
            else:
                socket_obj.close()
                return True
        
        def find_interface(interfaces):
            """returns the type of connection"""
            gateways = netifaces.gateways()
            result = list(
                filter(lambda x: (x == gateways["default"][2][1]), interfaces)
            )
            if len(result) < 1:
                logger.exception(f"{self}; interfaces not found.")
                return None
            return result[0]
            
        if ping():
            network = find_interface(self.interfaces)
            if not network:
                return None
            elif network[:1] == "e":
                return "Ethernet"
            elif network[:1] == "w":
                return "Wifi"
        else:
            return "NO CONNECTION"

    def draw(self):
        self.drawer.clear(self.background or self.bar.background)

        match self.parse_connection():
            case "Wifi":
                self.draw_wifi()
            case "Ethernet":
                self.draw_ether()
            case _:
                self.draw_ether(disconnected=True)

        self.drawer.draw(
            offsetx=self.offset,
            offsety=self.offsety,
            width=self.length
        )

    def draw_ether(self, disconnected=False):
        mp = self.margin + self.padding
        self.drawer.set_source_rgb(
            self.foreground if self.foreground else "d5d5d5"
        )
        self._rounded_rect(
            mp,
            self.bar.height / 2 - self.WIDTH / 2,
            self.WIDTH,
            self.HEIGHT / 2,
            1
        )
        self.drawer.ctx.move_to(
            mp + self.WIDTH / 2,
            self.bar.height / 2
        )
        self.drawer.ctx.line_to(
            mp + self.WIDTH / 2,
            self.bar.height / 2 + self.HEIGHT / 2
        )
        self.drawer.ctx.stroke()

        if disconnected:
            self.drawer.set_source_rgb("000000")
            self.drawer.ctx.set_line_width(1)
            self.drawer.ctx.move_to(
                mp + self.WIDTH,
                self.bar.height / 2 - self.HEIGHT / 2
            )
            self.drawer.ctx.line_to(
                mp,
                self.bar.height / 2 + self.HEIGHT / 2
            )
            self.drawer.ctx.stroke()

            self.drawer.set_source_rgb("ff0000")
            self.drawer.ctx.set_line_width(2)
            self.drawer.ctx.move_to(
                mp + self.WIDTH,
                self.bar.height / 2 - self.HEIGHT / 2 + 0.5
            )
            self.drawer.ctx.line_to(
                mp,
                self.bar.height / 2 + self.HEIGHT / 2 + 0.5
            )
            self.drawer.ctx.stroke()

            self.drawer.set_source_rgb("000000")
            self.drawer.ctx.set_line_width(1)
            self.drawer.ctx.move_to(
                mp + self.WIDTH,
                self.bar.height / 2 - self.HEIGHT / 2 + 1
            )
            self.drawer.ctx.line_to(
                mp,
                self.bar.height / 2 + self.HEIGHT / 2 + 1
            )
            self.drawer.ctx.stroke()

    def draw_wifi(self):
        y_margin = self.bar.height / 2 + self.HEIGHT /2
        self.drawer.set_source_rgb(
            self.foreground if self.foreground else "d5d5d5"
        )
        self.drawer.ctx.set_line_width(1.5)
        self.drawer.ctx.arc(
            self.length / 2,
            y_margin - self.HEIGHT / 10,
            (self.HEIGHT - self.HEIGHT * 0.75) - self.HEIGHT / 10,
            0,
            math.pi * 2
        )
        self.drawer.ctx.fill()
        self.drawer.ctx.arc(
            self.length / 2,
            y_margin,
            self.HEIGHT - self.HEIGHT / 2,
            220 * (math.pi / 180),
            -40 * (math.pi / 180)
        )
        self.drawer.ctx.new_sub_path()
        self.drawer.ctx.arc(
            self.length / 2,
            y_margin,
            self.HEIGHT - self.HEIGHT / 4,
            220 * (math.pi / 180),
            -40 * (math.pi / 180)
        )
        self.drawer.ctx.new_sub_path()
        self.drawer.ctx.arc(
            self.length / 2,
            y_margin,
            self.HEIGHT,
            220 * (math.pi / 180),
            -40 * (math.pi / 180)
        )
        self.drawer.ctx.stroke()

    def _rounded_rect(self, x, y, width, height, linewidth):
        aspect = 0.8
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

    def timer_setup(self):
        self.draw()
        if self.update_interval is not None:
            self.timeout_add(self.update_interval, self.timer_setup)

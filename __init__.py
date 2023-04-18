from .clickable_clock import ClickableClock
from .vpn import VPN
from .battery import Battery
from .volume import Volume

widget_defaults = dict(
    font="FiraCode Nerd Font Mono",
    fontsize=16,
    padding=3,
)

__all__ = [
    "widget_defaults",
    "ClickableClock",
    "VPN",
    "Battery",
    "Volume"
]

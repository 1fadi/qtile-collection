from .clickable_clock import ClickableClock
from .vpn import VPN
from .battery import Battery
from .volume import Volume
from .network import Network

widget_defaults = dict(
    font="FiraCode Nerd Font Mono",
    fontsize=16,
    padding=8,
)

__all__ = [
    "widget_defaults",
    "ClickableClock",
    "VPN",
    "Battery",
    "Volume",
    "Network"
]

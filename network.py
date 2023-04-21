from libqtile.widget import base
from libqtile.log_utils import logger

from utils import connection


class Network(base.ThreadPoolText):
    """requires a nerd font to display icons."""

    defaults = [
        ("interfaces", [], "network interfaces"),
        ("update_interval", 30, "time between updates"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(Network.defaults)
        
    def _update_string(self):
        result = self._get_info()
        match result:
            case "Wi-fi":
                return ""
            case "Ethernet":
                return "󰛳"
            case _:
                return ""

    def _get_info(self):
        return connection(self.interfaces)

    def poll(self):
        return self._update_string()

from libqtile.widget import base
import subprocess


class VPN(base.ThreadPoolText):
    """a simple widget to display vpn connection."""

    defaults = [
        (
            "on",
            "VPN",
            "string to indicate the device is connected to VPN"
        ),
        (
            "off",
            "",
            "string to indicate the device is not connected to VPN."
        ),
    ]

    def __init__(self, **config) -> None:
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(VPN.defaults)

    def poll(self):
        process = subprocess.run(
            "ip a | grep tun0 | grep inet | wc -l",
            capture_output=True,
            text=True,
            shell=True,
        )
        return self.on if int(process.stdout.strip()) else self.off

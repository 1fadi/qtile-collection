from libqtile.widget import Volume as Vlm


class Volume(Vlm):

    def _update_drawer(self):
        if self.volume <= 0:
            self.text = "󰸈"
        elif self.volume <= 50:
            self.text = "󰖀"
        elif self.volume <= 100:
            self.text = "󰕾"


from libqtile.widget.clock import Clock


class ClickableClock(Clock):
    def __init__(self, time_format=None, date_format=None, **config):
        self.time_format = time_format if time_format else "%H:%M:%S"
        self.date_format = date_format if date_format else "%A, %B %d, %Y"
        self.format = self.time_format

        self.date_format = date_format
        self.show_date = False
        super().__init__(**config)

        self.add_callbacks({
            "Button1": self.toggle_date,
        })

    def toggle_date(self):
        self.show_date = not self.show_date
        if self.show_date:
            self.format = self.date_format
        else:
            self.format = self.time_format
        self.update(self.poll())

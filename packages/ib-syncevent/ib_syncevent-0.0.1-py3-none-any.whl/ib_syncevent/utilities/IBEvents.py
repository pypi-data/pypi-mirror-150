from typing import Callable


class IBEvents():
    def __init__(self):
        self.historical_bars_event: Callable or None = None

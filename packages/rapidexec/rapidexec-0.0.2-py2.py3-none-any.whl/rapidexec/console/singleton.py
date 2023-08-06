from rich.live import Live


class LiveDisplaySingleton:
    _live = None

    @classmethod
    def go_online(cls, console):
        if cls._live is None:
            cls._live = Live(screen=True, console=console, refresh_per_second=4)
        return cls._live

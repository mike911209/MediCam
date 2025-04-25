# nevikw39

from collections.abc import Callable
from threading import Timer, Event


def interval(sec: int, event: Event = None):

    def decorator(func: Callable):
        timer: Timer

        def wrapper(*args, **kwargs):
            if event and event.is_set(): return

            func(*args, **kwargs)

            nonlocal timer
            timer = Timer(sec, wrapper)
            timer.start()

        return wrapper

    return decorator

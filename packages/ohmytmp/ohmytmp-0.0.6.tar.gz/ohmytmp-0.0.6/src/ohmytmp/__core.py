import os
from typing import Callable
from copy import deepcopy as dcp

from .__constant import FUNC, Info
from .__plugin import PluginBase
from .__guesstype import guesstype


class Ohmytmp:
    def __init__(self) -> None:
        self.func = {i: list() for i in FUNC.to_dict().values()}
        self.reg_f(guesstype, FUNC.GUESSTYPE)

    def register(self, a: PluginBase) -> None:
        try:
            event = a.event
        except AttributeError:
            event = FUNC.AFTER
        if event is None:
            event = FUNC.AFTER

        try:
            level = a.level
        except AttributeError:
            level = -1

        self.reg_f(a.func, event, level)

    def reg_f(self, func: Callable, event: str = FUNC.AFTER, level: int = -1) -> None:
        if level == -1:
            self.func[event].append(func)
            return
        if level < 0:
            level += 1
        self.func[event] = self.func[event][:level] + \
            [func,] + self.func[event][level:]

    def reg_handle(self, event: str = FUNC.AFTER, level: int = -1):
        def __get_f(f: Callable):
            def __new_f(*args, **kwds):
                return f(*args, **kwds)
            self.reg_f(__new_f, event, level)
            return __new_f
        return __get_f

    def init_file(self, p: str) -> Info:
        info = Info(p)
        for i in sorted(self.func):
            if i < FUNC.AFTER:
                for j in self.func[i]:
                    j(info)
            else:
                for j in self.func[i]:
                    j(dcp(info))
        return info

    def walk(self, d: str):
        for p, _, f in os.walk(d):
            for i in f:
                self.init_file(os.path.join(p, i))


__all__ = ('Ohmytmp',)

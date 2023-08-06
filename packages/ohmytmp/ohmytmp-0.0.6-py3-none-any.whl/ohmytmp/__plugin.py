from typing import Callable

from .__constant import Info, FUNC


class PluginBase:
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        event: int = None,
        level: int = -1,
    ) -> None:
        self.event = event
        self.level = level
        if func is not None:
            self.func = func

    def func(self, *l, **d):
        pass


class PluginGuessType(PluginBase):
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        level: int = -1,
    ) -> None:
        super().__init__(func, FUNC.GUESSTYPE, level)

    # def func(self, info: Info) -> None:
    #     pass


class PluginAnalysis(PluginBase):
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        level: int = -1,
    ) -> None:
        super().__init__(func, FUNC.ANALYSIS, level)

    # def func(self, info: Info) -> None:
    #     pass


class PluginAddTags(PluginBase):
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        level: int = -1,
    ) -> None:
        super().__init__(func, FUNC.ADDTAGS, level)

    # def func(self, info: Info) -> None:
    #     pass


class PluginDestination(PluginBase):
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        level: int = -1,
    ) -> None:
        super().__init__(func, FUNC.DESTINATION, level)

    # def func(self, info: Info) -> None:
    #     pass


class PluginAfter(PluginBase):
    def __init__(
        self,
        func: Callable[[Info], None] = None,
        level: int = -1,
    ) -> None:
        super().__init__(func, FUNC.AFTER, level)

    # def func(self, _info: Info) -> None:
    #     pass


__all__ = ('PluginBase', 'PluginGuessType', 'PluginAnalysis',
           'PluginAddTags', 'PluginDestination', 'PluginAfter')

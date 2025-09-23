import abc
from typing_extensions import Literal

class FormalGameInterface(metaclass=abc.ABCMeta):
    # @classmethod
    # def __subclasshook__(cls, subclass):
    #     return (
    #         hasattr(subclass, 'getWinStatus') and
    #         callable(subclass.getWinStatus)
    #     )
    @abc.abstractmethod
    def getWinStatus(self) -> Literal["win", "ongoing"]:
        """Return the current win status of the game."""
        pass

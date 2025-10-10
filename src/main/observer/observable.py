from main.observer.game_observer import GameObserver

import abc

class Observable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def addObserver(self, gameObserver: GameObserver) -> None:
        pass
    
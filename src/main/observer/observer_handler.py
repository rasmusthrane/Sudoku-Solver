from main.observer.game_observer import GameObserver

from typing import List

class ObserverHandler:
    def __init__(self) -> None:
        self.observerList: List[GameObserver] = []

    def addObserver(self, observer: GameObserver) -> None:
        self.observerList.append(observer)

    def notifySetCellValue(self, cell:str, value:str) -> None:
        for gameObserver in self.observerList:
            gameObserver.onSettingCellValue(cell, value)
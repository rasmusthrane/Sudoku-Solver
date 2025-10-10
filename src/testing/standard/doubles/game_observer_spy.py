from main.observer.game_observer import GameObserver

from typing import override

class GameObserverSpy(GameObserver):
    def __init__(self) -> None:
        self.lastCalledOnSettingCellValue: str = ""

    @override
    def onSettingCellValue(self, cell: str, value: str) -> None:
        self.lastCalledOnSettingCellValue = f"placed {value} in {cell}"
    def getOnSettingCellValue(self) -> str:
        return self.lastCalledOnSettingCellValue
from main.observer.game_observer import GameObserver

from typing import override

class GameObserverImpl(GameObserver):
    @override
    def onSettingCellValue(self, cell: str, value: str) -> None:
        pass
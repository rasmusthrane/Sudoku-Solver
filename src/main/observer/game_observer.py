import abc

class GameObserver(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def onSettingCellValue(self, cell:str, value:str) -> None:
        """
        Invoked when setCellValue() returns OK.
        """
        pass
from main.framework.game import FormalGameInterface

class TestHelper:

    @staticmethod
    def printGameState(game: FormalGameInterface):
        print("=== Game State Print ===")

    @staticmethod
    def printHighlight(any: object):
        RED = "\033[91m"
        BOLD = "\033[1m"
        RESET = "\033[0m"

        print(f"{BOLD}{RED}{'='*20}")
        print(any)
        print(f"{'='*20}{RESET}")


if __name__ == "__main__":
    testHelper = TestHelper()
    testHelper.printHighlight("hi")


from .handlers.chesscomhandlers.dailypuzzlehandler import PuzzleHandler, PuzzleInfo


class PuzzleFactory(object):
    """A class to create a chess.com puzzle, that can be the daily puzzle or a random puzzle"""

    def __init__(self) -> None:
        self.puzzleHandler = PuzzleHandler()
        pass

    def getDaily(self):
        """Gets the puzzle of the day, which is the daily"""
        return Puzzle(self.puzzleHandler.getDaily())

    def getRandomPuzzle(self):
        """Gets a random puzzle"""
        return Puzzle(self.puzzleHandler.getRandomPuzzle())

class Puzzle(object):
    """A class to represent a chess.com puzzle"""
    def __init__(self, info: PuzzleInfo) -> None:
        self.info = info
    

import functools
from typing import Optional

from .models.teammatch.teammatchboardinfo import TeamMatchBoardInfo
from .handlers.chesscomhandlers.teammatchboardhandler import TeamMatchBoardHandler


class TeamMatchBoard(object):
    """A class to represent a chess.com team match board"""

    def __init__(self, boardUrl, lazy = True):
        """Initializes a TeamMatchBoard object with the given boardUrl, the fetches will be based on that boardUrl"""
        self.boardUrl = boardUrl
        if lazy == False:
            self.info
    
    @functools.cached_property
    def info(self):
        return self._getInfo()

    def _getInfo(self) -> Optional[TeamMatchBoardInfo]:
        return TeamMatchBoardHandler().getInfo(self.boardUrl)



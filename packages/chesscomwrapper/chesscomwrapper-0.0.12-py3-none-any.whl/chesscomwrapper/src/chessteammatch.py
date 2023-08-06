import functools
from .handlers.chesscomhandlers.teammatchhandler import TeamMatchHandler


class TeamMatch(object):
    """A class to represent a chess.com team match"""

    def __init__(self, urlId, lazy = True) -> None:
        """Initializes a TeamMatch object with the given urlId, the fetches will be based on that urlId"""
        self.urlId = urlId
        if lazy == False:
            self.info

    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    def _getInfo(self):
        return TeamMatchHandler().getInfo(self.urlId)
    


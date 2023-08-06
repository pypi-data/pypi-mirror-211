import functools
from typing import Optional

from .models.tournament.tournamentinfo import TournamentInfo
from .handlers.chesscomhandlers.tournamenthandler import TournamentHandler


class Tournament(object):
    """A class to represent a chess.com tournament"""

    def __init__(self, id, lazy = True):
        """Initializes a Tournament object with the given id, the fetches will be based on that id"""
        self.id = id
        if lazy == False:
            self.info
        
    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    
    def _getInfo(self) -> Optional[TournamentInfo]:
        return TournamentHandler().getInfo(self.id)





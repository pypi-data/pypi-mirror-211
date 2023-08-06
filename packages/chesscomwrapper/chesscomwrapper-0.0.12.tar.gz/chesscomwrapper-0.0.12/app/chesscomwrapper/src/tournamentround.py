import functools
from typing import Optional
from .handlers.chesscomhandlers.roundhandler import RoundHandler
from .models.tournament.tournamnetroundinfo import TournamentRoundInfo


class TournamentRound(object):
    """A class to represent a chess.com tournament round"""
    def __init__(self, url, lazy = True):
        """Initializes a TournamentRound object with the given url, the fetches will be based on that url"""
        self.url = url
        if lazy == False:
            self.info

    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    def _getInfo(self) -> Optional[TournamentRoundInfo]:
        return RoundHandler().getInfo(self.url)

    
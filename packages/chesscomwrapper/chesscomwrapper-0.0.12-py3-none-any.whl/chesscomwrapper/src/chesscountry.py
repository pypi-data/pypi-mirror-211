from typing import Optional
from .chessplayer import ChessPlayer

from .models.country.countryinfo import CountryInfo
from .chessclub import Club
from .handlers.chesscomhandlers.countryhandler import CountryHandler
import functools


class ChessCountry(object):
    """A class to represent a chess.com country"""

    def __init__(self, abbr, lazy = True) -> None:
        """Initializes a ChessCountry object with the given abbreviation, the fetches will be based on that abbreviation"""
        self.code = abbr
        if lazy == False:
            self.info
            self.players
            self.clubs

    @functools.cached_property
    def info(self):
        return self._getInfo()
    
    @functools.cached_property
    def players(self):
        return self._getPlayers()
    
    @functools.cached_property
    def clubs(self):
        return self._getClubs()
    
    def _getInfo(self) -> Optional[CountryInfo]:
        return CountryHandler().getInfo(self.code)

    def _getPlayers(self) -> Optional[list[ChessPlayer]]:
        return CountryHandler().getPlayers(self.code)
    
    def _getClubs(self) -> Optional[list[Club]]:
        return CountryHandler().getClubs(self.code)
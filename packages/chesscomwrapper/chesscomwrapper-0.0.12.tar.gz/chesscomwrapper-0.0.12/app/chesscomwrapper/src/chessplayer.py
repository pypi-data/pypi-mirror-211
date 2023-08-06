from typing import Optional

from .models.player.titledcategory import TitledCategory

from .models.player.playerclub import PlayerClub

from .models.player.playertournament import PlayerTournaments
from .playerarchive import PlayerArchive
from .handlers.chesscomhandlers.playerhandler import PlayerHandler, PlayerHandlerInterface
from .models.player.chessplayerstats import ChessPlayerStats
from .models.player.chessplayerprofile import ChessPlayerProfile
from .models.player.playergames import ChesscomGame, ChesscomGameToMove
import functools


    


class ChessPlayer(object):
  """A class to represent a chess.com player"""

  ##the handler for the requests to the chess.com API regarding a player
  handler: PlayerHandlerInterface = PlayerHandler()

  def __init__(self, username: str, lazy:bool =True):
    """Initializes a ChessPlayer object with the given username, the fetches will be based on that username
    @param username the username of the player
    """
    
    ## the value of the username
    self.username = username
    if lazy == False:
      self.profile
      self.stats
      self.games
      self.gamesToMove
      self.tournaments
      self.clubs
      self.archives
    pass
  
  ## the profile informations of the player
  @functools.cached_property
  def profile(self) -> Optional[ChessPlayerProfile]:
    """
    @return a ChessPlayerProfile object if the player exists, otherwise returns None
    """
    return self._getProfile()
  
  ## the stats of the player regarding the different time controls
  @functools.cached_property
  def stats(self) -> Optional[ChessPlayerStats]:
    """
    @return a ChessPlayerStats object if the player exists, otherwise returns None
    """
    return self._getStats()
  
  ## the games the player is playing
  @functools.cached_property
  def games(self) -> Optional[list[ChesscomGame]]:
    """
    @return a list of ChesscomGame objects rapresenting the games he is playing if there are, otherwise returns None
    """
    return self._getPlayerGames()
  
  ## the games the player has to move
  @functools.cached_property
  def gamesToMove(self) -> Optional[list[ChesscomGameToMove]]:
    """
    @return a list of ChesscomGameToMove objects if there are, otherwise returns None
    """
    return self._getPlayerGamesToMove()
  
  ## the tournaments the player has played or is playing
  @functools.cached_property
  def tournaments(self) -> Optional[PlayerTournaments]:
    """
    @return a PlayerTournaments object if there are, otherwise returns None
    """
    return self._getPlayerTournaments()

  ## the clubs the player is enrolled in
  @functools.cached_property
  def clubs(self) -> Optional[list[PlayerClub]]:
    """
    @return a list of PlayerClub objects the player is enrolloed in, otherwise returns None
    """
    return self._getPlayerClubs() 

  ## the archives of the player's games
  @functools.cached_property
  def archives(self) -> Optional[list[PlayerArchive]]:
    """
    @return a list of PlayerArchive objects with the history of his games, otherwise returns None
    """
    return self._getPlayerArchives() 

  

  def _getProfile(self) -> Optional[ChessPlayerProfile]:
    """
    @return a ChessPlayerProfile object if the player exists, otherwise returns None
    """
    
    return self.handler.getPlayerProfile(self.username)
    
  
  def _getStats(self) -> Optional[ChessPlayerStats]:
    """
    @return a ChessPlayerStats object if the player exists, otherwise returns None
    """
    return self.handler.getPlayerStats(self.username)
    
  def _getPlayerGames(self) -> Optional[list[ChesscomGame]]:
    """
    @return a list of ChesscomGame objects if there are, otherwise returns None
    """
    return self.handler.getPlayerGames(self.username)

  def _getPlayerGamesToMove(self) -> Optional[list[ChesscomGameToMove]]:
    """
    @return a list of ChesscomGameToMove objects if there are, otherwise returns None
    """
    return self.handler.getPlayerGamesToMove(self.username)
  
  def _getPlayerArchives(self) -> Optional[list[PlayerArchive]]:
    """
    @return a list of PlayerArchive objects with the history of his games, otherwise returns None
    """
    return self.handler.getPlayerArchives(self.username)
  
  def _getPlayerTournaments(self) -> Optional[PlayerTournaments]:
    """
    @return a PlayerTournaments object if there are, otherwise returns None
    """
    return self.handler.getPlayerTournaments(self.username)

  def _getPlayerClubs(self) -> Optional[list[PlayerClub]]:
    """
    @return a list of PlayerClub objects the player is enrolloed in, otherwise returns None
    """
    return self.handler.getPlayerClubs(self.username)
  
  @staticmethod
  def _getTitledPlayers(self, category: TitledCategory):
    """
    @param category: the category of the titled players to get

    @return a list of ChessPlayer objects with the players of the given category
    """

    return list(map(lambda player: ChessPlayer(player),self.handler.getTitledPlayers(category)))

""" @brief A class to wrap the chess.com API 
    @mainpage Chess.com API Wrapper
    @section intro_sec Introduction
    This package is a wrapper for the chess.com API. It provides a set of classes to interact with the API.
    The API is documented here: https://www.chess.com/news/view/published-data-api and it is the source of the data used in this package.
    @section notes_sec Notes
    - Copyright (c) 2023 Nicola Panozzo.  All rights reserved.
"""

# imports
import sys

from .models.leaderboards.leaderboardsinfo import LeaderboardsInfo

from .models.streamer.chessstreamerinfo import ChessStreamerInfo

from .models.player.titledcategory import TitledCategory


from .chessstreamer import ChessStreamer






sys.path.append("/Users/nicolapanozzo/unibo/Kaunas Courses/Component Based Software Engineering/chesscom_api_wrapper")

from .chessclub import Club
from .chessplayer import ChessPlayer 
from .chesstournament import Tournament
from .chessteammatch import TeamMatch
from .chesscountry import ChessCountry
from .dailypuzzle import Puzzle, PuzzleFactory

from .chessleaderboards import ChessLeaderboards
class ChesscomWrapper(object):
  """A class to wrap the chess.com API"""
  
  def __init__(self):
    pass
  


  def getPlayer(self,username: str, lazy: bool = True) -> ChessPlayer:
    """Returns a chess player
    @param username: The username of the player (e.g. "hikaru")
    @param lazy: If True, the player's data is not fetched until the first time the data is accessed. If False, the data is fetched immediately.

    @return A ChessPlayer object
    """
    player = ChessPlayer(username, lazy)

    return player
  
  def getClub(self, clubname: str, lazy=True) -> Club:
    """Returns a Club
    @type clubname: str
    @param clubname The name of the club (e.g. "bonobo")

    @return A Club object
    """
    club = Club(clubname, lazy)
    return club
  
  def getTournament(self, tournamentUrl: str) -> Tournament:
    """Returns a tournament
    @param tournamentId The id of the tournament (e.g. "https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600")

    @return A Tournament object
    """
    tournament = Tournament(tournamentUrl)
    return tournament
  
  def getTeamMatch(self, matchUrl: str) -> TeamMatch:
    """Returns a team match
    @param matchUrl The url of the team match (e.g. "https://api.chess.com/pub/match/1250" is referring to "https://www.chess.com/club/matches/kaunas-university-of-technology/1250")

    @return A TeamMatch object
    """
    teamMatch = TeamMatch(matchUrl)
    return teamMatch
  
  def getTitledPlayers(self, category: TitledCategory) -> list[ChessPlayer]:
    """Returns titled players
    @param category The category of titled players to return (e.g. TitledCategory.GM)

    @return A list of ChessPlayer objects
    """
    return ChessPlayer._getTitledPlayers(self, category)
    
  def getCountry(self, countryCode: str) -> ChessCountry:
    """Returns a country
    @param countryCode The code of the country (e.g. "IT")
    
    @return A ChessCountry object
    """
    return ChessCountry(countryCode)
  
  def getDailyPuzzle(self) -> Puzzle:
    """Returns the daily puzzle
    
    @return A Puzzle object
    """
    return PuzzleFactory().getDaily()
  
  def getRandomPuzzle(self) -> Puzzle:
    """Returns a random puzzle
    
    @return A Puzzle object
    """
    return PuzzleFactory().getRandomPuzzle()
  
  def getStreamersInfo(self) -> list[ChessStreamerInfo]:
    """Returns a list of streamers
    
    @return A list of ChessStreamerInfo objects"""
    return ChessStreamer._getStreamersInfo(self)
  
  def getLeaderboards(self) -> LeaderboardsInfo:
    """Returns a list of streamers

    @return A LeaderboardsInfo object
    """
    return ChessLeaderboards().getLeaderboards()
  



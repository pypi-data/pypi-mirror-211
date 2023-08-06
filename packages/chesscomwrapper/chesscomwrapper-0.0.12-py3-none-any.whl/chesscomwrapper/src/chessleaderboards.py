from .handlers.chesscomhandlers.leaderboardshandler import LeaderboardsHandler
from .models.leaderboards.leaderboardsinfo import LeaderboardsInfo


class ChessLeaderboards(object):
    """A class to represent the chess.com leaderboards"""
    
    @staticmethod
    def getLeaderboards() -> LeaderboardsInfo:
        """Gets all the leaderboards from Chess.com"""
        return LeaderboardsHandler().getLeaderboards()
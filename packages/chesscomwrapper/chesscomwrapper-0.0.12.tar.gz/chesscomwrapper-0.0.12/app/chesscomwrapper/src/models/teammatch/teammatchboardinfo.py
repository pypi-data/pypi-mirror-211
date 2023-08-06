from ..player.playergames import ChesscomGameArchived


class TeamMatchBoardInfo(object):
    """Represents a chess.com team match board info with  scores and games"""
    def __init__(self, data):
        self.board_scores = BoardScores(data.get('board_scores', None))
        self.games = [ChesscomGameArchived(game) for game in data.get('games', [])]

class BoardScores(object):
    """Represents a chess.com team match board scores with player1, player2 and result"""
    def __init__(self, data):
        # get the value of the first key
        self.player1 = list(data.keys())[0]
        self.player1Score = data.get(list(data.keys())[0], None)
        self.player2 = list(data.keys())[1]
        self.player2Score = data.get(list(data.keys())[1], None)
        self.result = f'{self.player1Score}-{self.player2Score}'


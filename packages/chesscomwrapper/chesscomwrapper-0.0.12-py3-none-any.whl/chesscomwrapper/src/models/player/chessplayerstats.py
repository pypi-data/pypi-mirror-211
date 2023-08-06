class ChessPlayerStats:
    """ Represents a chess player's stats for every time control"""

    def __init__(self, data):
        if not data:
            return None
        """Initializes a ChessPlayerStats object"""

        self.chess_daily = ChessVariant(data.get("chess_daily", None))
        self.chess960_daily = ChessVariant(data.get("chess960_daily", None))
        self.chess_rapid = ChessVariant(data.get("chess_rapid", None))
        self.chess_bullet = ChessVariant(data.get("chess_bullet", None))
        self.chess_blitz = ChessVariant(data.get("chess_blitz", None))
        self.fide = data.get("fide", None)
        self.tactics = Tactics(data.get("tactics", None))
        self.puzzle_rush = PuzzleRush(data.get("puzzle_rush", None))
        self.puzzle_rush_daily = PuzzleRush(data.get("puzzle_rush_daily", None))

class ChessVariant:
    """ Represents a chess variant """
    def __init__(self, data):
        if not data:
            return None
        self.last = ChessRating(data.get("last"))
        self.best = ChessBest(data.get("best"))
        self.record = ChessRecord(data.get("record"))
        self.tournament = ChessTournament(data.get("tournament"))

class ChessRating:
    """ Represents a chess rating """
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)
        self.rd = data.get("rd", None)

class ChessBest:
    """ Represents a chess best rating"""
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)
        self.game = data.get("game", None)

class ChessRecord:
    """ Represents a chess record with wins, losses, draws, time per move, and timeout percent"""
    def __init__(self, data):
        if not data:
            return None
        self.win = data.get("win", None)
        self.loss = data.get("loss", None)
        self.draw = data.get("draw", None)
        self.time_per_move = data.get("time_per_move", None)
        self.timeout_percent = data.get("timeout_percent", None)

class ChessTournament:
    """ Represents a chess tournament with points, withdraw, count, and highest finish"""
    def __init__(self, data):
        if not data:
            return None
        self.points = data.get("points", None)
        self.withdraw = data.get("withdraw", None)
        self.count = data.get("count", None)
        self.highest_finish = data.get("highest_finish", None)

class Tactics:
    """ Represents a tactics rating with highest and lowest score"""
    def __init__(self, data):
        if not data:
            return None
        self.highest = TacticsRating(data.get("highest", None))
        self.lowest = TacticsRating(data.get("lowest", None))

class TacticsRating:
    """ Represents a tactics rating with score and date"""
    def __init__(self, data):
        if not data:
            return None
        self.rating = data.get("rating", None)
        self.date = data.get("date", None)

class PuzzleRush:
    """ Represents a puzzle rush score with best score"""
    def __init__(self, data):
        if not data:
            return None
        self.best = PuzzleRushScore(data.get("best", None))

class PuzzleRushScore:
    """ Represents a puzzle rush score with score and total attempts taken"""
    def __init__(self, data):
        if not data:
            return None
        self.total_attempts = data.get("total_attempts", None)
        self.score = data.get("score", None)
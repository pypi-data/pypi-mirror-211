class API():
    """A class to store API endpoints for chess.com"""
    # PLAYER API (PLAYER_BASE + username (+ ?))

    ## the base url for the chess.com API
    BASE_URL = "https://api.chess.com/pub/"
    
    PLAYER_BASE = BASE_URL + "player/"
    STATS = "stats/"
    GAMES = "games/"
    GAMES_TO_MOVE = "games/to-move/"
    GAMES_ARCHIVES = "games/archives/"
    GAMES_MONTHLY_ARCHIVES = "games/YEAR/MONTH/"
    PGN = "pgn/"
    CLUB = "club/"
    CLUBS = "clubs/"
    TOURNAMENTS = "tournaments/"
    TITLED_PLAYERS = "titled/"
    COUNTRY = "country/"
    PLAYERS = "players/"
    PUZZLE = "puzzle/"
    RANDOM = "random/"
    STREAMERS = "streamers/"
    LEADERBOARDS = "leaderboards/"


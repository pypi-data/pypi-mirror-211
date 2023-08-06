from ..player.playergames import ChesscomGameArchived
from ..tournament.tournamentroundplayer import TournamentRoundPlayer


class TournamentRoundGroupInfo(object):
    """A class to represent a tournament round group info with fair play removals, games and players"""
    def __init__(self, data):
        self.fair_play_removals = data.get('fair_play_removals', None)
        self.games = [ChesscomGameArchived(gamedata) for gamedata in data.get('games', [])]
        self.players = [TournamentRoundPlayer(playerdata) for playerdata in data.get('players', [])]
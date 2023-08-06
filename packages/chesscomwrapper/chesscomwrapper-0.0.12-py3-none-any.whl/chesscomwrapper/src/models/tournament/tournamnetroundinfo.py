from ..tournament.tournamentroundplayer import TournamentRoundPlayer
from ...tournamentroundgroup import TournamentRoundGroup

class TournamentRoundInfo(object):
    """A class to represent a tournament round info with groups and players"""
    def __init__(self, data):
        self.groups = [TournamentRoundGroup(group) for group in data.get('groups', [])] 
        self.players = [TournamentRoundPlayer(playerdata) for playerdata in data.get('players', [])] 
    
    

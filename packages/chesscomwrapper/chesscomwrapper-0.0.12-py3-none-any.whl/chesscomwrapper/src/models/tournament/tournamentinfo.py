from ..tournament.tournamentsettings import TournamentSettings
from ..tournament.tournamentplayer import TournamentPlayer
from ...tournamentround import TournamentRound


class TournamentInfo(object):
    """A class to represent a tournament info with the id, name, url, description, creator, status, finish time, settings, players and rounds"""
    def __init__(self, data) -> None:
        self.id = data.get('@id', None)
        self.name = data.get('name', None)
        self.url = data.get('url', None)
        self.description = data.get('description', None)
        self.creator = data.get('creator', None)
        self.status = data.get('status', None)
        self.finish_time = data.get('finish_time', None)
        self.settings = TournamentSettings(data.get('settings', None))
        self.players = [TournamentPlayer(playerdata) for playerdata in data.get('players', None)]
        self.rounds = [TournamentRound(url) for url in data.get('rounds', None)]

class TournamentPlayer(object):
    """A class to represent a player in a tournament with the username and status"""
    def __init__(self, data) -> None:
        self.username = data.get('username', None)
        self.status = data.get('status', None)
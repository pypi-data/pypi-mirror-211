class TournamentRoundPlayer(object):
    """A class to represent a tournament round player with the username, points, is advancing and tie break"""
    def __init__(self, data):
        self.username = data.get('username', None)
        self.points = data.get('points', None)
        self.is_advancing = data.get('is_advancing', None)
        self.tie_break = data.get('tie_break', None)
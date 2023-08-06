class PlayerTournaments(object):
    """Represents a list of tournaments a player is in """
    def __init__(self, data):
        self.finished = list(map(lambda finishedData: PlayerTournamentFinished(finishedData), data.get('finished', None)))
        self.inProgress = list(map(lambda registeredData: PlayerTournamentInProgress(registeredData), data.get('in_progress', None)))
        self.registered = list(map(lambda registeredData: PlayerTournamentRegistered(registeredData), data.get('registered', None)))




class PlayerTournamentRegistered(object):
    ''' Represents a tournament that a player is registered in '''
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)


class PlayerTournamentInProgress(object):
    ''' Represents a tournament in progress that a player is in '''
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)
        self.totalPlayers = data.get('total_players', None)
        self.wins = data.get('wins', None)
        self.losses = data.get('losses', None)
        self.draws = data.get('draws', None)


class PlayerTournamentFinished(object):
    ''' Represents a completed tournament that a player has participated in '''
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.url = data.get('url', None)
        self.status = data.get('status', None)
        self.totalPlayers = data.get('total_players', None)
        self.placement = data.get('placement', None)
        self.wins = data.get('wins', None)
        self.losses = data.get('losses', None)
        self.draws = data.get('draws', None)
        self.pointsAwarded = data.get('points_awarded', None)
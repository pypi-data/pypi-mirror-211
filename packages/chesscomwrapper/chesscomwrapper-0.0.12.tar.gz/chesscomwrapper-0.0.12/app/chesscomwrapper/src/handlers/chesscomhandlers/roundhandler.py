from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler
from ..chesscomhandler import ChesscomHandler
from ...models.tournament.tournamnetroundinfo import TournamentRoundInfo


class RoundHandler(ChesscomHandler):
    """A class to handle the requests to the chess.com API regarding a round"""
    def __init__(self):
        """Initializes a RoundHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getInfo(self, url):
        """Returns player's monthly archives"""
        response = self.doRequest(url)
        if response is None:
            return None
        roundinfo = TournamentRoundInfo(response.json())
        return roundinfo

    
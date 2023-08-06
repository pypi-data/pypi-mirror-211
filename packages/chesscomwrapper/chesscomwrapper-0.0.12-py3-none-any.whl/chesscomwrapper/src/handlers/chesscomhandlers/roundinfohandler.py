from ..errorhandlers.noneerrorhandler import NoneErrorHandler
from ..requesthandlers.singletonrequesthandler import SingletonRequestHandler
from ..chesscomhandler import ChesscomHandler
from ...models.tournament.tournamentroundgroupinfo import TournamentRoundGroupInfo


class RoundInfoHandler(ChesscomHandler):
    """A class to handle the requests to the chess.com API regarding a round"""
    def __init__(self):
        """Initializes a RoundHandler object"""
        self.errorHandler = NoneErrorHandler()
        self.requestHandler = SingletonRequestHandler()
        pass


    def getRoundGroupInfo(self, url):
        """Returns player's monthly archives"""
        response = self.doRequest(url)
        if response is None:
            return None
        roundinfo = TournamentRoundGroupInfo(response.json())
        return roundinfo

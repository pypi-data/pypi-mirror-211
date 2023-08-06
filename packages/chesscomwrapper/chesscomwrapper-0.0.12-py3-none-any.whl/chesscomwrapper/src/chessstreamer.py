from .handlers.chesscomhandlers.streamerhandler import StreamerHandler
from .models.streamer.chessstreamerinfo import ChessStreamerInfo


class ChessStreamer(object):
    """A class to represent a chess.com streamer"""

    @staticmethod
    def _getStreamersInfo(self):
        """Gets a list of streamers"""
        return StreamerHandler().getStreamersInfo()


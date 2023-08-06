from ...chessplayer import ChessPlayer


class ClubMember(object):
    """Represents a member of a club with the username and the date when the player joined the club"""
    def __init__(self, username, joined) -> None:
        self.player = ChessPlayer(username)
        self.joined = joined

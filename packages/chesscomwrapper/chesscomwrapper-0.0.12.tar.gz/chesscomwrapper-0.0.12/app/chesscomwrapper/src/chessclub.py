from typing import Optional

from .models.club.clubprofile import ClubProfile
from .models.player.playerclub import PlayerClub
from .models.club.clubmember import ClubMember
from .handlers.chesscomhandlers.clubhandler import ClubHandler, ClubHandlerInterface
import functools


class Club(object):
    """A class to represent a chess.com club"""

    ## the handler for the requests to the chess.com API regarding a club
    handler: ClubHandlerInterface = ClubHandler()


    def __init__(self, clubname: str, lazy: bool = True) -> None:
        """Initializes a Club object with the given clubname, the fetches will be based on that clubname
        @param clubname the name of the club"""
        self.id = clubname
        if lazy == False:
            self.profile
            self.members
        

    ## the profile informations of the club
    @functools.cached_property
    def profile(self):
        return self._getProfile()
    
    @functools.cached_property
    def members(self):
        return self._getMembers()
    
    
    def _getMembers(self) -> Optional[list[ClubMember]]:
        return self.handler.getMembers(self.id)
    
    def _getProfile(self) -> Optional[ClubProfile]:
        return self.handler.getProfile(self.id)


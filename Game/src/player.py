import random
from point import Point

#
# Represents a playable character
#
class Player:

    ALIVE = "alive"
    DEAD = "dead"
    EXITED = "exited"

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = self.ALIVE
        self.game_state = None
        self.location = None
        self.health = 3

    # 
    # Returns how to render the player on the map
    # -> String
    #
    def render(self):
        return self.name[0]

    #
    # Updates the player's status
    # String -> void
    #
    def set_status(self, status):
        self.status = status

    #
    # Returns the player's health
    # -> int
    #
    def get_health(self):
        return self.health

    #
    # Updates the player's health
    # int -> void
    #
    def set_health(self, health):
        self.health = health
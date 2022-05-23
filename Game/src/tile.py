#
# The representation of a tile in hallways and rooms
#
class Tile:

    # Temporary characters to represent tiles in map rendering
    ROOM_WALL = "x"
    ROOM_FLOOR = "o"
    DOOR = "d"
    HALLWAY_FLOOR = "f"
    VOID = " "
    EXIT = "e"
    KEY = "k"

    def __init__(self, attribute):
        self.attribute = attribute
        self.item = None
        self.player = None
        self.adversary = None

    #
    # Sets this tile's item to exit
    # -> void
    #
    def place_exit(self):
        self.item = self.EXIT
    
    #
    # Sets this tile's item to key
    # -> void
    #
    def place_key(self):
        self.item = self.KEY

    #
    # Sets this tile's item to none
    # -> void
    #
    def remove_item(self):
        self.item = None
    
    #
    # Sets this tile's player to a Player object
    # Player -> void
    #
    def place_player(self, player):
        self.player = player

    #
    # Sets this tile's player to none
    # -> void
    #
    def remove_player(self):
        self.player = None

    #
    # Sets this tile's adversary to an Adversary object
    # Adversary -> void
    #
    def place_adversary(self, adversary):
        self.adversary = adversary

    #
    # Sets this tile's adversary to none
    # -> void
    #
    def remove_adversary(self):
        self.adversary = None

    #
    # Returns the representation when rendered
    # -> string
    #
    def render(self):
        if self.player:
            return self.player.render()
        elif self.adversary:
            return self.adversary.render()
        elif self.item:
            return self.item
        else:
            return self.attribute

    #
    # Determines if the tile is empty
    # -> bool
    #
    def tile_empty(self):
        return not self.item and not self.adversary and not self.player
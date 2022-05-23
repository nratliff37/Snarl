from tile import *

#
# The representation of a room in a level
#
class Room:

    def __init__(self, origin, layout):
        self.origin = origin
        self.tiles = {}
        if self.validate_layout(layout):
            self.initialize_tiles(layout)

    #
    # Validates whether a given layout can be made into a room
    # string -> boolean
    #
    def validate_layout(self, layout):
        valid = True
        # Check that a floor exists
        if Tile.ROOM_FLOOR not in layout:
            return False

        lines = layout.splitlines()

        length = len(lines[0])
        for line in lines:
            valid = valid and (length == len(line))
        
        # Check boundaries
        for tile in lines[0]:
            valid = valid and (tile == Tile.ROOM_WALL or tile == Tile.DOOR)
        for tile in lines[-1]:
            valid = valid and (tile == Tile.ROOM_WALL or tile == Tile.DOOR)
        for line in lines:
            valid = valid and (line[0] == Tile.ROOM_WALL or line[0] == Tile.DOOR) and (line[-1] == Tile.ROOM_WALL  or line[-1] == Tile.DOOR)


        # Set length and width of room based on layout
        if valid:
            self.length = length
            self.width = len(lines)
        return valid

    #
    # Converts the given layout into tiles
    # string -> void
    #
    def initialize_tiles(self, layout):
        lines = layout.splitlines()

        for x in range (len(lines)):
            for y in range (len(lines[x])):
                key = self.generate_key(x, y)
                self.tiles[key] = Tile(lines[x][y])

    #
    # Returns a key string representing the tile coordinates relative to the origin
    # int int -> string
    #
    def generate_key(self, x, y):
        key = str(self.origin.x + x) + "," + str(self.origin.y + y)
        return key

    #
    # Returns the available tiles in the room
    # -> Tile{}
    #
    def available_tiles(self):
        available_tiles = {}

        for key, tile in self.tiles.items():
            if tile.attribute == Tile.ROOM_FLOOR and tile.tile_empty():
                available_tiles[key] = tile

        return available_tiles

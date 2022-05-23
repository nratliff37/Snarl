from room import Room
from hallway import Hallway
from tile import Tile
from point import Point

#
# The representation of a level in a dungeon
#
class Level:

    def __init__(self):
        self.rooms = {}
        self.hallways = {}
        self.tiles = {}
        self.key_found = False

    #
    # Adds a room to the level if it is valid
    # Point String -> void
    #
    def add_room(self, origin, layout):
        room = Room(origin, layout)

        if self.validate_room(room) and room.tiles:
            self.rooms[str(origin)] = room
            self.tiles.update(room.tiles)

    #
    # Adds a hallway to the level if it is valid
    # Point Point Point[] -> void
    #    
    def add_hallway(self, endpoint_1, endpoint_2, waypoints):
        key_1 = str(endpoint_1)
        key_2 = str(endpoint_2)

        tile_1 = self.tiles[key_1]
        tile_2 = self.tiles[key_2]

        if tile_1.attribute == Tile.DOOR and tile_2.attribute == Tile.DOOR:
            hallway = Hallway(endpoint_1, endpoint_2, waypoints)

            if self.validate_hallway(hallway) and hallway.tiles:
                hall_key = key_1 + ' ' + key_2
                self.hallways[hall_key] = hallway
                self.tiles.update(hallway.tiles)

    #
    # Places a key on the tile matching the point
    # Point -> void
    #
    def place_key(self, point):
        key = str(point)
        if self.tiles[key].attribute == Tile.ROOM_FLOOR:
            self.tiles[key].place_key()
    
    #
    # Places an exit on the tile matching the point
    # Point -> void
    #
    def place_exit(self, point):
        key = str(point)
        if self.tiles[key].attribute == Tile.ROOM_FLOOR:
            self.tiles[key].place_exit()

    #
    # Validates whether a new room can be added to this level
    # room -> boolean
    #
    def validate_room(self, room):
        valid = True
        for tile in room.tiles.keys():
            if (valid and tile not in self.tiles):
                continue
            else:
                return False
        return valid
    
    #
    # Validates whether a new hallway can be added to this level
    # room -> boolean
    #
    def validate_hallway(self, hallway):
        valid = True
        for tile in hallway.tiles.keys():
            if tile == str(hallway.endpoint_1) or tile == str(hallway.endpoint_2):
                continue
            elif (valid and tile not in self.tiles):
                continue
            else:
                return False
        return valid
    
    #
    # Returns a dictionary of the coords for the upperleftmost and bottomrightmost coordinates
    # -> Dictionary
    #
    def get_corners(self):
        keys = self.tiles.keys()
        
        x_coords = []
        y_coords = []

        for key in keys:
            coords = key.split(",")
            x_coords.append(int(coords[0]))
            y_coords.append(int(coords[1]))
        
        x_coords.sort()
        y_coords.sort()

        corners = {
            "smallest_x": x_coords[0],
            "biggest_x": x_coords[-1],
            "smallest_y": y_coords[0],
            "biggest_y": y_coords[-1]
        }

        return corners
    
    #
	# Places player to the tile at the given point
	# Player Point -> void
	#
    def place_player(self, player, point):
        self.tiles[str(point)].place_player(player)

    #
    # Removes player from the tile at the given point
    # Point -> void
    #
    def remove_player(self, point):
        self.tiles[str(point)].remove_player()

    #
	# Moves player to the tile at the given point
	# Player Point Point -> void
	#
    def move_player(self, player, fro, to):
        self.remove_player(fro)
        self.place_player(player, to)

    #
	# Places adversary to the tile at the given point
	# Adversary Point -> void
	#
    def place_adversary(self, adversary, point):
        self.tiles[str(point)].place_adversary(adversary)

    #
    # Removes adversary from the tile at the given point
    # Point -> void
    #
    def remove_adversary(self, point):
        self.tiles[str(point)].remove_adversary()

    #
	# Moves adversary to the tile at the given point
	# Adversary Point Point -> void
	#
    def move_adversary(self, adversary, fro, to):
        self.remove_adversary(fro)
        self.place_adversary(adversary, to)

    #
    # Renders the entire level to STDOUT
    # -> STDOUT
    #
    def render_map(self):
        corners = self.get_corners()
        map = ""

        for x in range(corners["smallest_x"], corners["biggest_x"] + 1):
            for y in range(corners["smallest_y"], corners["biggest_y"] + 1):
                key = str(x) + "," + str(y)
                render_tile = self.tiles.get(key)
                if render_tile:
                    map = map + render_tile.render()
                else:
                    map = map + " "
            map = map + "\n"

        print(map)

    #
    # Returns the available tiles in the level
    # -> Tile{}
    #
    def available_tiles(self):
        available_tiles = {}

        for key, room in self.rooms.items():
            room_tiles = room.available_tiles()
            available_tiles.update(room_tiles)

        return available_tiles
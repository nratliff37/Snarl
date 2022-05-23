from point import Point
from tile import Tile

#
# The representation of a hallway in a level
#
class Hallway:

    def __init__(self, endpoint_1, endpoint_2, waypoints):
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2
        self.waypoints = waypoints 
        self.tiles = {}
        self.initialize_tiles()

    #
    # Calculates the route based on the given endpoints and waypoints to generate tiles
    # -> void
    #
    def initialize_tiles(self):

        # No waypoints
        if not self.waypoints:
            point_list = self.endpoint_1.get_intermediate_points(self.endpoint_2)
            point_list.append(self.endpoint_2)
        # Waypoints exists
        else:
            point_list = self.endpoint_1.get_intermediate_points(self.waypoints[0])

            for i in range(len(self.waypoints) - 1):
                points = self.waypoints[i].get_intermediate_points(self.waypoints[i + 1])
                point_list.extend(points)

            final_points = self.waypoints[-1].get_intermediate_points(self.endpoint_2)
            point_list.extend(final_points)
            point_list.append(self.endpoint_2)
        
        for point in point_list:
            key = self.generate_key(point.x, point.y)
            self.tiles[key] = Tile(Tile.HALLWAY_FLOOR)
        
        # Set the doors
        self.tiles[str(self.endpoint_1)].attribute = Tile.DOOR
        self.tiles[str(self.endpoint_2)].attribute = Tile.DOOR

    
    #
    # DEPRECTATED 
    # Generates the wall tiles around the hallway path
    # -> void
    #
    def build_walls(self):
        wall_tiles = {}

        for tile in self.tiles.keys():
            if tile != str(self.endpoint_1) and tile != str(self.endpoint_2):
                coords = tile.split(",")
                point = Point(coords[0], coords[1])

                # List of Points
                neighbors = point.neighbors()

                for neighbor in neighbors:
                    key = str(neighbor)
                    if key not in self.tiles:
                        wall_tiles[str(neighbor)] = Tile(Tile.HALLWAY_WALL)
        self.tiles.update(wall_tiles)

    #
    # Generates a key string based off given coordinate
    # int int -> string
    #
    def generate_key(self, x, y):
        key = str(x) + "," + str(y)
        return key
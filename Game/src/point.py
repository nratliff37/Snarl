from tile import Tile

#
# The representation of a coordinate point on the level grid
#
class Point:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
    #
    # Returns list of points between this point and the given point
    # Point -> Point[]
    #
    def get_intermediate_points(self, other_point):
        point_list = []

        # Determine if horizontal or vertical
        if (self.x == other_point.x):
            # Vertical
            if (self.y < other_point.y):
                for i in range(self.y, other_point.y):
                    point = Point(self.x, i)
                    point_list.append(point)
            else:
                for i in range(other_point.y, self.y):
                    point = Point(self.x, self.y - (i - other_point.y))
                    point_list.append(point)
        else:
            # Horizontal
            if (self.x < other_point.x):
                for i in range(self.x, other_point.x):
                    point = Point(i, self.y)
                    point_list.append(point)
            else:
                for i in range(other_point.x, self.x):
                    point = Point(self.x - (i - other_point.x), self.y)
                    point_list.append(point)

        return point_list
    
    #
    # Returns a new point of the sum
    # Point -> Point
    #
    def add(self, point):
        new_x = self.x + point.x
        new_y = self.y + point.y
        return Point(new_x, new_y)

    #
    #
    # Point -> [int, int]
    #
    def point_to_array(self):
        return [self.x, self.y]

    
    #
    # Returns the surrounding 4 neighbors of a point
    # -> Point[]
    #
    def neighbors(self):
        up = Point(self.x, self.y - 1)
        right = Point(self.x + 1, self.y)
        left = Point(self.x - 1, self.y)
        down = Point(self.x, self.y + 1)

        neighbors = [up, right, left, down]
        return neighbors
    
    def __str__(self):
        return str(self.x) + "," + str(self.y)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y
    
    #
    # Returns the 5x5 area around a given point based on the tiles given
    # Tile{} -> Int[][]
    #
    def layout_list(self, tiles):
        layout_list = []

        top_left_x = self.x - 2
        top_left_y = self.y - 2
        
        for i in range (5):
            row_list = []

            for j in range (5):
                point = Point(top_left_x + i, top_left_y + j)
                tile = tiles.get(str(point), Tile(Tile.VOID))

                if tile.attribute == Tile.ROOM_WALL:
                    row_list.append(0)
                elif tile.attribute == Tile.ROOM_FLOOR or tile.attribute == Tile.HALLWAY_FLOOR:
                    row_list.append(1)
                elif tile.attribute == Tile.DOOR:
                    row_list.append(2)
                else:
                    row_list.append(0)

            layout_list.append(row_list)

        return layout_list

    #
    # Returns the tiles in the 5x5 radius around the player
    # Tile{} -> Tile{}
    #
    def player_vision(self, tiles):
        tile_map = {}

        top_left_x = self.x - 2
        top_left_y = self.y - 2
        
        for i in range (5):
            for j in range (5):
                point = Point(top_left_x + i, top_left_y + j)
                tile = tiles.get(str(point), None)

                if tile:
                    tile_map[str(point)] = tile

        return tile_map
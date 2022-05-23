from point import Point
from player import Player
from user_client import UserClient

#
# Represents a User
# DEPRECATED, ONLY NETWORKED USERS WORK NOW
#
class User(UserClient):


    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.player = Player(id, name)
        self.tiles = {}
        self.location = None

    def begin_turn(self, message):
        self.tiles = message["tiles"]
        print("\nSTART OF TURN FOR PLAYER " + str(self.id) + " : " + self.name)
        print("-------------------------------")
        self.render()

        available_moves = message["moveable_tiles"]
        available_moves.append("")
        print("Current Location: " + str(self.location))
        print("Available Moves: " + str(available_moves))
        return self.send_message(available_moves)


    def send_message(self, available_moves):
        to = input("Enter your move: ")
        
        while to not in available_moves:
            print("Not a valid move!")
            to = input("Enter your move: ")

        if to == '':
            to_arr = self.location.point_to_array()
        else:
            to_arr = to.split(",")
        
        response_json = {
            "player": self.name,
            "from": self.location.point_to_array(),
            "to": to_arr
        }

        return response_json 

    def receive_update(self, update):
        self.tiles = update["tiles"]

        if update["player_id"] != None:
            print("\nRESULT OF PLAYER " + str(update["player_id"]) + " TURN")
            print("-------------------------------")
        
        if update["tiles"]:
            self.render()

        message = update["result"]
        if message:
            print(message)

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

    def render(self):
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

    

    
import socket
import json
from point import Point
from player import Player
from user_client import UserClient


class NetworkUser(UserClient):

    def __init__(self, id, name, socket):
        self.id = id
        self.name = name
        self.player = Player(id, name)
        self.tiles = {}
        self.location = None
        self.socket = socket
        print(self.socket)


    #
    # Called to begin a user's turn with a given message and receive their next move
    # String -> ResponseJSON
    #
    def begin_turn(self, message):        
        
        self.socket.sendall(json.dumps(message).encode())
        player_move_str = self.socket.recv(1024)
        print(player_move_str)
        player_move = json.loads(player_move_str)
        
        if player_move["type"] == "move":
            to = player_move["to"]
            if to != None:
                response_json = {
                    "player": self.name,
                    "from": self.location.point_to_array(),
                    "to": to
                }
                return response_json
            else:
                response_json = {
                    "player": self.name,
                    "from": self.location.point_to_array(),
                    "to": self.location.point_to_array()
                }
                return response_json 

    # Send the result of the User's move to them
    def send_result(self, result):
        self.socket.sendall(result.encode())

    # Send the update of any action to the User
    def receive_update(self, update):
        self.socket.sendall(json.dumps(update).encode())

    # Tell the User the level is starting
    def start_level(self, start_level):
        self.socket.sendall(json.dumps(start_level).encode())
    
    # Tell the User the level is ending
    def end_level(self, end_level):
        self.socket.sendall(json.dumps(end_level).encode())
    
    # Tell the User the game is over
    def end_game(self, end_game):
        self.socket.sendall(json.dumps(end_game).encode())
    
    # Unused
    def render(self):
        pass

    # Unused
    def send_message(self):
        pass

    

        

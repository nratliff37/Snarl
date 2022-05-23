from game_state import GameState
from player import Player
from adversary import Adversary
from point import Point
from rulechecker import RuleChecker
from user import User
from observer import Observer
from zombie import Zombie
from ghost import Ghost
from tile import Tile
from network_user import NetworkUser
import random
import math

class GameManager:

    def __init__(self, total_levels, level_JSON):
        self.users = []
        self.exit_scores = {}
        self.key_scores = {}
        self.adversaries = []
        self.observers = []
        self.game_state = GameState()
        self.rulechecker = RuleChecker(self.game_state)
        self.total_levels = total_levels
        self.level_JSON = level_JSON
        self.key_holder = None
        
    #
    # Adds a user to this game with unique name
    # string -> void
    #
    def add_user(self, name):
        if (len(self.users) < 4):
            unique_name = True
            for user in self.users:
                unique_name = unique_name and (name != user.name)
            if unique_name:
                id = len(self.users)
                self.users.append(User(id, name))
    
    #
    # Adds a user to this game with unique name
    # string -> void
    #
    def add_network_user(self, name, socket):
        if (len(self.users) < 4):
            unique_name = True
            for user in self.users:
                unique_name = unique_name and (name != user.name)
            if unique_name:
                id = len(self.users)
                self.users.append(NetworkUser(id, name, socket))
    
    #
    # Adds a adversary to this game with unique name
    # string, string -> void
    #
    def add_adversary(self, name, type):
        unique_name = True
        for adversary in self.adversaries:
            unique_name = unique_name and (name != adversary.name)
        if unique_name:
            if type == Adversary.ZOMBIE:
                self.adversaries.append(Zombie(name))
            elif type == Adversary.GHOST:
                self.adversaries.append(Ghost(name))

    def add_observer(self):
        self.observers.append(Observer())

    #
    # Manually override and set the level
    # level -> void
    #
    def set_level(self, level):
        self.game_state.level = level

    #
    # Handles the player's turn
    # User -> void
    #
    def process_player_turn(self, user):
        starting_location = user.player.location

        # Send a message to player -> 
        # Receives a message from player <-
        response = user.begin_turn("move")

        # Translates player's response
        fro = response["from"]
        to = response["to"]

        # Handle player's move
        result = None
        to_point = Point(to[0], to[1])
        if self.rulechecker.validate_move_player(user.player, to_point):
            self.game_state.move_player(user.player, to_point)
            self.users[user.player.id].location = to_point
            result = "OK"
        else:
            result = "Invalid"

        interact_result = self.game_state.interact_player(user.player)
        if interact_result != None:
            result = interact_result
        
        result_response = user.send_result(result)

        if result == ("Key"):
            score = self.key_scores.get(user.player.name, 0)
            score = score + 1
            self.key_scores[user.player.name] = score
            self.key_holder = user.player.name

        if result == ("Damage -1"):
            self.game_state.move_player(user.player, starting_location)
            self.users[user.player.id].location = starting_location
        
        self.send_updates(result)
        
        for observer in self.observers:
            observer.update(self.game_state)

    #
    # Handles the adversary's turn
    # -> void
    #
    def process_adversary_turn(self, adversary):
        starting_location = adversary.location

        response = adversary.begin_turn(self.game_state)

        # Handle player's move
        to_point = Point(response[0], response[1])
        if self.rulechecker.validate_move_adversary(adversary, to_point):
            self.game_state.move_adversary(adversary, to_point)
        
        result = self.game_state.interact_adversary(adversary)

        if result == ("Damage -1"):
            self.game_state.move_adversary(adversary, starting_location)

        # Tell everyone
        self.send_updates(result)
        
        for observer in self.observers:
            observer.update(self.game_state)

    #
    # DEPRECATED
    # Sets up the level and places all players into a predetermined spot
    # Level, Point[], Point[], Point, Point -> void
    #
    def setup_game(self, level, player_locations, adversary_locations, key_location, exit_location):
        self.set_level(level)

        # Place the players
        for user in self.users:
            self.game_state.add_player(user.player)
            player = user.player

            # Place player in predetermined spot
            # Will be more random once we have further information on level generation
            if self.rulechecker.validate_place_player(player_locations[player.id]):
                self.game_state.place_player(player, player_locations[player.id])
                user.location = player_locations[player.id]

        # Place the adversaries
        for location in adversary_locations:
            if self.rulechecker.validate_place_adversary(location):
                self.add_adversary("Adversary " + str(len(self.adversaries)))
                adversary = self.adversaries[-1]
                self.game_state.add_adversary(adversary)
                self.game_state.place_adversary(adversary, location)

        # Place the key
        if key_location:
            self.game_state.level.place_key(key_location)

        # Place the exit
        if exit_location:
            self.game_state.level.place_exit(exit_location)

    #
    # Function that runs the main game loop
    # -> void
    #
    def game_loop(self):

        while (True):
            level = self.game_state.current_level
            if self.rulechecker.game_won():
                self.level_won()

                if level == self.total_levels:
                    print("Game Won! Congratulations!")
                    print("-------------------------------")
                    self.game_over()
                else:
                    next_level = self.game_state.current_level + 1
                    self.start_game(next_level)
                    pass
                break
            if self.rulechecker.all_dead():
                print("Game over! You failed on Level " + str(level) + ".")
                self.game_over()
                break
            
            for user in self.users:
                if user.player.status == Player.ALIVE:
                    # Process player turn
                    self.process_player_turn(user)
            for adversary in self.adversaries:
                # Process adversary turn
                self.process_adversary_turn(adversary)


    #
    # Starts the game setup and loop
    # int -> void
    #
    def start_game(self, starting_level):
        self.game_state = GameState()
        self.rulechecker = RuleChecker(self.game_state)
        self.generate_level(starting_level)
        self.generate_players()
        self.generate_adversaries()
        self.send_start_level()
        self.send_updates(None)
        self.game_loop()

    #
    # Adds a room using the given format to our game format
    # RoomJSON -> void
    #
    def add_room(self, room_json):  
        origin_arr = room_json["origin"]

        layout_array_converted = []

        layout_arr = room_json["layout"]
        for y in layout_arr:
            row = []
            for x in y:
                if x == 0:
                    row.append(Tile.ROOM_WALL)
                elif x == 1:
                    row.append(Tile.ROOM_FLOOR)
                elif x == 2:
                    row.append(Tile.DOOR)
            layout_array_converted.append(row)

        room = { "type": "room",
                 "origin": origin_arr,
                 "layout": layout_array_converted}
        return room

    #
    # Adds a hallway using the given format to our game format
    # RoomJSON -> void
    #
    def add_hallway(self, hallway_json):
        from_arr = hallway_json["from"]
        to_arr = hallway_json["to"]
        waypoints = hallway_json["waypoints"]
        
        hallway = { "type": "hallway",
                    "endpoint_1": from_arr,
                    "endpoint_2": to_arr,
                    "waypoints": waypoints }
        return hallway

    #
    # Converts a point to an array
    # Point -> [int, int]
    #
    def point_to_array(self, point):
        return [point.x, point.y]

    #
    # Converts an array to a point
    # [int, int] -> Point
    #
    def array_to_point(self, arr):
         return Point(arr[0], arr[1])

    #
    # Return all of the reachable tiles from the given Point
    # Point -> Tile[]
    #
    def reachable_tiles(self, point):
        neighbors = point.neighbors()
        reachable_tiles = []

        for neighbor in neighbors:
            neighbor_tile = self.game_state.level.tiles.get(str(neighbor), False)
            if neighbor_tile:
                if neighbor_tile.attribute == Tile.ROOM_FLOOR or neighbor_tile.attribute == Tile.HALLWAY_FLOOR or neighbor_tile.attribute == Tile.DOOR:
                    if neighbor_tile.player == None:
                        reachable_tiles.append(str(neighbor))
                    neighbors_2 = neighbor.neighbors()
                    for neighbor_2 in neighbors_2:
                        neighbor_2_tile = self.game_state.level.tiles.get(str(neighbor_2), False)
                        if neighbor_2_tile:
                            if neighbor_2_tile.attribute == Tile.ROOM_FLOOR or neighbor_2_tile.attribute == Tile.HALLWAY_FLOOR or neighbor_2_tile.attribute == Tile.DOOR:
                                if neighbor_2 not in reachable_tiles:
                                    if neighbor_2_tile.player == None:
                                        reachable_tiles.append(str(neighbor_2))

        return list(set(reachable_tiles))

    #
    # Returns all the objects visible in a set of tiles
    # Tile{} -> Item[]
    #
    def objects_in_vision(self, tiles):
        visible_objects = []
        for key, tile in tiles.items():
            if tile.item:
                point_arr = key.split(",")
                point_arr = [int(point_arr[0]), int(point_arr[1])]
                item = ""
                if tile.item == Tile.KEY:
                    item = "key"
                elif tile.item == Tile.EXIT:
                    item = "exit"
                item_position = {
                    "type": item,
                    "position": point_arr
                }
                visible_objects.append(item_position)
        return visible_objects
    
    #
    # Returns all the actors visible in a set of tiles
    # Tile{} -> Actor[]
    #
    def actors_in_vision(self, tiles):
        visible_actors = []
        for key, tile in tiles.items():
            if tile.player:
                actor_position = {
                                "type": "player",
                                "name": tile.player.name,
                                "position": tile.player.location.point_to_array()
                            }
                visible_actors.append(actor_position)
            elif tile.adversary:
                actor_position = {
                                "type": tile.adversary.type,
                                "name": tile.adversary.name,
                                "position": tile.adversary.location.point_to_array()
                            }
                visible_actors.append(actor_position)
        return visible_actors

    #
    # Returns a list of names of all users
    # -> String[]
    #
    def generate_name_list(self):
        name_list = []
        for user in self.users:
            name_list.append(user.name)

        return name_list

    #
    # Converts the result string into a more detailed version
    # String -> String
    #
    def result_string(self, result):
        return result
    
    #
    # Handles the logic when a level is won
    # -> void
    #
    def level_won(self):
        print("Level " + str(self.game_state.level) + " completed!")

        exited_players = []
        ejected_players = []
        for player in self.game_state.players:
            if player.status == Player.EXITED:
                score = self.exit_scores.get(player.name, 0)
                score = score + 1
                self.exit_scores[player.name] = score
                exited_players.append(player.name)
            else:
                ejected_players.append(player.name)

        for user in self.users:
            end_level = {
                "type": "end-level",
                "key": self.key_holder,
                "exits": exited_players,
                "ejects": ejected_players
            }
            user.end_level(end_level)
        self.key_holder = None
    
    #
    # Handles the logic when a game is over
    # -> void
    #
    def game_over(self):
        
        print(self.exit_scores)
        print(self.key_scores)

        exit_scores_sorted = []
        for key, score in self.exit_scores.items():
            score_str = str(score) + " - " + key
            exit_scores_sorted.append(score_str)
            exit_scores_sorted.sort(reverse=True)
                    
            print("Times Exited:")
            for score in exit_scores_sorted:
                print(score)

        
        key_scores_sorted = []    
        for key, score in self.key_scores.items():
            score_str = str(score) + " - " + key
            key_scores_sorted.append(score_str)
            key_scores_sorted.sort(reverse=True)

            print("Times Found Key:")
            for score in key_scores_sorted:
                print(score)
                    
        scores_send = []
        for user in self.users:
            player_score_list = {
                "type": "player-score",
                "name": user.name,
                "exits": self.exit_scores.get(user.name, 0),
                "ejects": self.game_state.current_level - self.exit_scores.get(user.name, 0),
                "keys": self.key_scores.get(user.name, 0)
            }
            scores_send.append(player_score_list)
            
        for user in self.users:
            end_game = {
                "type": "end-game",
                "scores": scores_send
            }
        user.end_game(end_game)
    
    # 
    # Generates the level with the given starting level
    # int -> void
    #
    def generate_level(self, starting_level):
        level_json = self.level_JSON[starting_level - 1]

        walkables = []
        rooms = level_json["rooms"]
        for room in rooms:
            walkable_json = self.add_room(room)
            walkables.append(walkable_json)

        hallways = level_json["hallways"]
        for hallway in hallways:
            walkable_json = self.add_hallway(hallway)
            walkables.append(walkable_json)

        self.game_state.set_level(starting_level, walkables)

        objects = level_json["objects"]
        for object in objects:
            typ = object["type"]
            point_arr = object["position"]
            point = self.array_to_point(point_arr)

            if typ == "key":
                self.game_state.level.place_key(point)
            elif typ == "exit":
                self.game_state.level.place_exit(point)

    #
    # Generates and places the users as players in the GameState
    # -> void
    #
    def generate_players(self):
        # Place the players
        for user in self.users:
            user.player.status = Player.ALIVE
            self.game_state.add_player(user.player)
            player = user.player

        players_placed = False
        while not players_placed:
            room_key = random.choice(list(self.game_state.level.rooms))
            room = self.game_state.level.rooms[room_key]
            tiles = room.available_tiles()
            
            if len(tiles) >= len(self.users):
                for user in self.users:
                    key = random.choice(list(tiles))
                    point_arr = key.split(",")
                    point = self.array_to_point(point_arr)

                    self.game_state.place_player(user.player, point)
                    user.location = point
                    del tiles[key]

                players_placed = True

    #
    # Generates and places the adversaries as players in the GameState
    # -> void
    #
    def generate_adversaries(self):
        # Place the adversaries
        level = self.game_state.current_level
        num_zombies = math.floor(level / 2) + 1
        num_ghosts = math.floor((level - 1) / 2)

        # Add Zombies
        for i in range(num_zombies):
            self.add_adversary("Zombie " + str(i + 1), Adversary.ZOMBIE)

        # Add Ghosts
        for i in range(num_ghosts):
            self.add_adversary("Ghost " + str(i + 1), Adversary.GHOST)

        adversaries_placed = False
        while not adversaries_placed:
            tiles = self.game_state.level.available_tiles()

            for adversary in self.adversaries:
                key = random.choice(list(tiles))
                point_arr = key.split(",")
                point = self.array_to_point(point_arr)

                self.game_state.place_adversary(adversary, point)
                del tiles[key]

            adversaries_placed = True
    
    #
    # Tell all Users a level has started 
    # -> void
    #
    def send_start_level(self):
        level_start = {
            "type": "start-level",
            "level": self.game_state.current_level,
            "players": self.generate_name_list()
        }
        for user in self.users:
            user.start_level(level_start)

    #
    # Tell all Users the most recent update
    # -> void
    #
    def send_updates(self, message):
        for user in self.users:
            # Tell everyone
            layout = user.location.layout_list(self.game_state.level.tiles)
            position = user.location.point_to_array()
            objects = self.objects_in_vision(user.location.player_vision(self.game_state.level.tiles))
            actors = self.actors_in_vision(user.location.player_vision(self.game_state.level.tiles))
            update = {
                "type": "player-update",
                "layout": layout,
                "position": position,
                "objects": objects,
                "actors": actors,
                "message": message
            }
            user.receive_update(update)
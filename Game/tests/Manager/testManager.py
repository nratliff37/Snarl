#!/usr/bin/env python3

import sys
import json
sys.path.insert(0, "../../src")
from tile import Tile
from rulechecker import RuleChecker
from point import Point
from player import Player
from adversary import Adversary
from level import Level
from game_state import GameState
from game_manager import GameManager
from user import User

class TestManager:
	  
	def __init__(self):
		self.manager = None
		self.level_json = None
		self.key_location = None
		self.exit_location = None
		self.test()


	#
	#
	# Point -> [int, int]
	#
	def success_message(self, manager_trace):
		players = []
		adversaries = []
		for user in self.manager.users:
			player = user.player
			if player.status == Player.ALIVE:
				player_json = {
					"type": "player",
					"name": player.name,
					"location": player.location.point_to_array()
				}
				players.append(player_json)
		for adversary in self.manager.adversaries:
			adversary_json = {
				"type": "zombie",
				"name": adversary.name,
				"location": adversary.location.point_to_array()
			}
			adversaries.append(adversary_json)
		state = {
			"type": "state",
			"level": self.level_json,
			"players": players,
			"adversaries": adversaries,
			"exit-locked": not self.manager.game_state.key_found
		}
		print(json.dumps([state, manager_trace]))
		return

	#
	#
	# Point -> [int, int]
	#
	def point_to_array(self, point):
		return [point.x, point.y]

	#
	#
	# [int, int] -> Point
	#
	def array_to_point(self, arr):
		 return Point(arr[0], arr[1])

	#
	#
	#
	#
	def add_room(self, room_json, level):
		origin_arr = room_json["origin"]
		origin = self.array_to_point(origin_arr)

		layout_str = ""

		layout_arr = room_json["layout"]
		for y in layout_arr:
			for x in y:
				if x == 0:
					layout_str = layout_str + Tile.ROOM_WALL
				elif x == 1:
					layout_str = layout_str + Tile.ROOM_FLOOR
				elif x == 2:
					layout_str = layout_str + Tile.DOOR
			layout_str = layout_str + "\n"

		level.add_room(origin, layout_str)

	#
	#
	#
	#
	def add_hallway(self, hallway_json, level):
		from_arr = hallway_json["from"]
		from_point = self.array_to_point(from_arr)
		to_arr = hallway_json["to"]
		to_point = self.array_to_point(to_arr)
		waypoints = []
		for waypoint in hallway_json["waypoints"]:
			waypoints.append(self.array_to_point(waypoint))
		level.add_hallway(from_point, to_point, waypoints)

	#
	#
	#
	#
	def object_locations(self, object_json):
		typ = object_json["type"]
		point_arr = object_json["position"]
		point = self.array_to_point(point_arr)

		if typ == "key":
			self.key_location = point
		elif typ == "exit":
			self.exit_location = point
	
	def player_update(self):
		trace_entries = []

		for user in self.manager.users:
			player = user.player

			if player.status == Player.ALIVE:
				layout = player.location.layout_list(player.game_state.level.tiles)
				tiles = player.location.player_vision(player.game_state.level.tiles)
				visible_objects = []
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
							"type": "zombie",
							"name": tile.adversary.name,
							"position": tile.adversary.location.point_to_array()
						}
						visible_actors.append(actor_position)
					elif tile.item:
						point_arr = key.split(",")
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

				player_update = {  "type" : "player-update",
								   "layout" : layout,
								   "position" : self.point_to_array(player.location),
								   "objects" : visible_objects,
								   "actors": visible_actors
								   }

				trace_entry = [player.name, player_update]
				trace_entries.append(trace_entry)

		return trace_entries

	def test(self):
		test_str = ""
		for line in sys.stdin:
			test_str += line
		test_json = json.loads(test_str)

		self.manager = GameManager()

		player_json = test_json[0]
		for player in player_json:
			self.manager.add_user(player)
		
		level_json = test_json[1]
		self.level_json = level_json
		level = Level()

		rooms_list = level_json["rooms"]
		hallways_list = level_json["hallways"]
		objects_list = level_json["objects"]

		for room in rooms_list:
			self.add_room(room, level)
		
		for hallway in hallways_list:
			self.add_hallway(hallway, level)
		
		for obj in objects_list:
			self.object_locations(obj)
		
		turn_number = test_json[2]
		point_list = test_json[3]

		player_locations = []
		adversary_locations = []
		for i in range (len(point_list)):
			if i < len(player_json):
				point_arr = point_list[i]
				point = self.array_to_point(point_arr)
				player_locations.append(point)
			else:
				point_arr = point_list[i]
				point = self.array_to_point(point_arr)
				adversary_locations.append(point)

		self.manager.setup_game(level, player_locations, adversary_locations, self.key_location, self.exit_location)

		manager_trace = []

		trace_entries = self.player_update()
		manager_trace = manager_trace + trace_entries

		actor_move_list_list = test_json[4]
		for i in range(turn_number):
			if not self.manager.rulechecker.game_won() and not self.manager.rulechecker.all_dead():
				for user in self.manager.users:
					player = user.player
					if player.status == Player.ALIVE:
						turn_over = False
						while not turn_over:
							if actor_move_list_list[player.id]:
								instruction = actor_move_list_list[player.id].pop(0)
								point_arr = instruction["to"]
								point = self.array_to_point(point_arr)

								if not point:
									turn_over = True
									entry = [player.name, instruction, "OK"]
									manager_trace.append(entry)
									trace_entries = self.player_update()
									manager_trace = manager_trace + trace_entries
								else:
									if self.manager.rulechecker.validate_move_player(player, point):
										self.manager.game_state.move_player(player, point)
										turn_over = True
										tile = self.manager.game_state.level.tiles[str(point)]
										message = ""
										if tile.adversary:
											message = "Eject"
										elif tile.item == Tile.KEY:
											message = "Key"
										elif tile.item == Tile.EXIT:
											message = "Exit"
										else:
											message = "OK"
										self.manager.game_state.interact_player(player)
										entry = [player.name, instruction, message]
											
										manager_trace.append(entry)
										trace_entries = self.player_update()
										manager_trace = manager_trace + trace_entries
									else:
										entry = [player.name, instruction, "Invalid"]
										manager_trace.append(entry)
										trace_entries = self.player_update()
										manager_trace = manager_trace + trace_entries
							else:
								# Terminate
								self.success_message(manager_trace)
								return
		self.success_message(manager_trace)


testManager = TestManager()
	
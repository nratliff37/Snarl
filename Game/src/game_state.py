from player import Player
from adversary import Adversary
from level import Level
from point import Point
from tile import Tile
import random

class GameState:

	def __init__(self):
		self.players = []
		self.player_locations = {}
		self.adversaries = []
		self.adversary_locations = {}
		self.current_level = -1
		self.level = None

	#
	# Adds a player to this game
	# -> void
	#
	def add_player(self, player):
		if (len(self.players) < 4):
			self.players.append(player)

	#
	# Adds an adversary to this game
	# -> void
	#
	def add_adversary(self, adversary):
		self.adversaries.append(adversary)

	#
	# Returns if the level's key has been found
	# -> boolean
	#
	def key_found(self):
		return self.level.key_found
	
	#
	# Places player to the tile at the given point
	# Player Point -> void
	#
	def place_player(self, player, point):
		self.level.place_player(player, point)
		self.player_locations[player.id] = point
		player.location = point

	#
	# Moves player to the tile at the given point
	# Player Point -> void
	#
	def move_player(self, player, point):
		self.level.move_player(player, self.player_locations[player.id], point)
		self.player_locations[player.id] = point
		player.location = point

	#
	# Places adversary to the tile at the given point
	# Adversary Point -> void
	#
	def place_adversary(self, adversary, point):
		self.level.place_adversary(adversary, point)
		self.adversary_locations[adversary.name] = point
		adversary.location = point

	#
	# Moves adversary to the tile at the given point
	# Adversary Point -> void
	#
	def move_adversary(self, adversary, point):
		self.level.move_adversary(adversary, self.adversary_locations[adversary.name], point)
		self.adversary_locations[adversary.name] = point
		adversary.location = point
		tile = self.level.tiles[str(point)]

		if tile.attribute == Tile.ROOM_WALL and adversary.type == Adversary.GHOST:
			key = random.choice(list(self.level.rooms))
			room = self.level.rooms[key]

			tile_key = random.choice(list(room.tiles))
			point_arr = tile_key.split(",")
			new_point = Point(point_arr[0], point_arr[1])
			new_point_tile = self.level.tiles[str(new_point)]

			if not new_point_tile.adversary:
				self.level.move_adversary(adversary, self.adversary_locations[adversary.name], new_point)
				self.adversary_locations[adversary.name] = new_point
				adversary.location = new_point

	#
	# Sets the current level to the given level_num, and initializes the level to the given rooms and hallways
	# int, Walkables_JSON[] -> void
	#
	def set_level(self, level_num, walkables):
		self.current_level = level_num
		level = Level()

		for walkable in walkables:
			walkable_type = walkable["type"]

			if walkable_type == "room":
				origin_array = walkable["origin"]
				origin_point = Point(origin_array[0], origin_array[1])

				layout_array = walkable["layout"]
				layout = ""
				for row in layout_array:
					for col in row:
						layout = layout + col
					layout = layout + "\n"

				level.add_room(origin_point, layout)
			elif walkable_type == "hallway":
				endpoint_1_array = walkable["endpoint_1"]
				endpoint_2_array = walkable["endpoint_2"]
				
				endpoint_1 = Point(endpoint_1_array[0], endpoint_1_array[1])
				endpoint_2 = Point(endpoint_2_array[0], endpoint_2_array[1])

				waypoints_JSON = walkable["waypoints"]
				waypoints = []
				for waypoint in waypoints_JSON:
					waypoint = Point(waypoint[0], waypoint[1])
					waypoints.append(waypoint)

				level.add_hallway(endpoint_1, endpoint_2, waypoints)

		self.level = level

	#
	# Returns a message that states the interaction.
	# Player -> str
	#
	def interact_player(self, player):
		point = self.player_locations[player.id]
		tile = self.level.tiles[str(point)]

		if tile.adversary:
			health = player.get_health()
			player.set_health(health - 1)

			# Checks if the player is dead
			if player.get_health() <= 0:
				player.set_status(Player.DEAD)
				tile.remove_player()
				return "Eject"
			else:
				return "Damage -1"
		elif tile.item == Tile.KEY:
			self.level.key_found = True
			tile.remove_item()
			return "Key"
		elif tile.item == Tile.EXIT:
			if self.key_found():
				player.set_status(Player.EXITED)
				tile.remove_player()
				return "Exit"
		return

	#
	# Returns a message that states the interaction
	# Adversary -> bool
	#
	def interact_adversary(self, adversary):
		point = self.adversary_locations[adversary.name]
		tile = self.level.tiles[str(point)]

		if tile.player:
			health = tile.player.get_health()
			tile.player.set_health(health - 1)

			# Checks if the player is dead
			if tile.player.get_health() <= 0:
				tile.player.set_status(Player.DEAD)
				name = tile.player.name
				tile.remove_player()
				return "Eject"
			else:
				return "Damage -1"

		return
		
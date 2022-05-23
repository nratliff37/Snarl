from adversary import Adversary
import random
from point import Point
from tile import Tile

#
# Represents a zombie
#
class Zombie(Adversary):

	VISION = 5

	def __init__(self, name):
		super().__init__(name, Adversary.ZOMBIE)

	#
	# Return how to render the ghost
	# -> String
	#
	def render(self):
		return "Z"

	#
	# Called to start the ghost's turn and receive their next move
	# GameState -> PointArr
	# 
	def begin_turn(self, state):
		self.game_state = state

		to = self.ai()
		return self.send_message(to)


	#
	# Determines the move that the Zombie will make
	# -> Point
	#
	def ai(self):
		nearest_player_location = self.nearest_player_location()

		if nearest_player_location:
			player_x = nearest_player_location.x
			player_y = nearest_player_location.y

			zombie_x = self.location.x
			zombie_y = self.location.y

			horizontal_diff = zombie_y - player_y
			vertical_diff = zombie_x - player_x

			moves = []

			# Right
			if horizontal_diff < 0:
				point = Point(zombie_x, zombie_y + 1)
				moves.append(point)
			# Left
			elif horizontal_diff > 0:
				point = Point(zombie_x, zombie_y - 1)
				moves.append(point)

			# Down
			if vertical_diff < 0:
				point = Point(zombie_x + 1, zombie_y)
				moves.append(point)
			# Up
			elif vertical_diff > 0:
				point = Point(zombie_x - 1, zombie_y)
				moves.append(point)

			valid_moves = []
			for point in moves:
				if self.validate_move(point):
					valid_moves.append(point)

			if len(valid_moves) == 0:
				return self.random_move()
			else:
				num = random.randint(0, len(valid_moves) - 1)
				point = valid_moves[num]
				return point

		else:
			return self.random_move()

	#
	# Moves the Zombie in a random direction and returns that point
	# -> Point
	#
	def random_move(self):
		valid_points = []
		neighbors = self.location.neighbors()

		for point in neighbors:
			if self.validate_move(point):
				valid_points.append(point)

		if len(valid_points) == 0:
			return self.location
		else:
			num = random.randint(0, len(valid_points) - 1)
			point = valid_points[num]
			return point

	#
	# Returns the point of the nearest player
	# -> Point
	#
	def nearest_player_location(self):
		zombie_location = self.location
		shortest_distance = self.VISION
		closest_point = None

		for key, location in self.game_state.player_locations.items():
			distance = abs(zombie_location.x - location.x) + abs(zombie_location.y - location.y)

			if distance <= shortest_distance:
				shortest_distance = distance
				closest_point = location

		return closest_point

	#
	# Sends a message to the GameManager
	# Point -> Point
	#
	def send_message(self, point):
		return point.point_to_array()

	#
	# Return whether or not the given adversary can move to the given point
	# Point -> boolean
	#
	def validate_move(self, point):
		to_tile = None
		try:
			to_tile = self.game_state.level.tiles[str(point)]
		except:
			return False
		
		neighbors = self.location.neighbors()
		reachable_tiles = []

		for neighbor in neighbors:
			neighbor_tile = self.game_state.level.tiles.get(str(neighbor), False)
			if neighbor_tile:
				if neighbor_tile.attribute == Tile.ROOM_FLOOR:
					if neighbor_tile.adversary == None:
						reachable_tiles.append(neighbor)
		
		return point in reachable_tiles
from adversary import Adversary
import random
from point import Point
from tile import Tile

#
# Represents a ghost
#
class Ghost(Adversary):

	VISION = 8

	def __init__(self, name):
		super().__init__(name, Adversary.GHOST)

	#
	# Return how to render the ghost
	# -> String
	#
	def render(self):
		return "G"

	#
	# Called to start the ghost's turn and receive their next move
	# GameState -> PointArr
	# 
	def begin_turn(self, state):
		self.game_state = state

		to = self.ai()
		return self.send_message(to)


	#
	# Determines the move that the Ghost will make
	# -> Point
	#
	def ai(self):
		nearest_player_location = self.nearest_player_location()

		if nearest_player_location:
			player_x = nearest_player_location.x
			player_y = nearest_player_location.y

			ghost_x = self.location.x
			ghost_y = self.location.y

			horizontal_diff = ghost_y - player_y
			vertical_diff = ghost_x - player_x

			moves = []

			# Right
			if horizontal_diff < 0:
				point = Point(ghost_x, ghost_y + 1)
				moves.append(point)
			# Left
			elif horizontal_diff > 0:
				point = Point(ghost_x, ghost_y - 1)
				moves.append(point)

			# Down
			if vertical_diff < 0:
				point = Point(ghost_x + 1, ghost_y)
				moves.append(point)
			# Up
			elif vertical_diff > 0:
				point = Point(ghost_x - 1, ghost_y)
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
			wall = self.nearest_wall_location()

			wall_x = wall.x
			wall_y = wall.y

			ghost_x = self.location.x
			ghost_y = self.location.y

			horizontal_diff = ghost_y - wall_y
			vertical_diff = ghost_x - wall_x

			moves = []

			# Right
			if horizontal_diff < 0:
				point = Point(ghost_x, ghost_y + 1)
				moves.append(point)
			# Left
			elif horizontal_diff > 0:
				point = Point(ghost_x, ghost_y - 1)
				moves.append(point)

			# Down
			if vertical_diff < 0:
				point = Point(ghost_x + 1, ghost_y)
				moves.append(point)
			# Up
			elif vertical_diff > 0:
				point = Point(ghost_x - 1, ghost_y)
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

	#
	# Moves the Ghost in a random direction and returns that point
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
		ghost_location = self.location
		shortest_distance = self.VISION
		closest_point = None

		for key, location in self.game_state.player_locations.items():
			distance = abs(ghost_location.x - location.x) + abs(ghost_location.y - location.y)

			if distance <= shortest_distance:
				shortest_distance = distance
				closest_point = location

		return closest_point

	#
	# Returns the point of the nearest wall
	# -> Point
	#
	def nearest_wall_location(self):
		seen = [self.location]
		unseen = self.location.neighbors()

		while True:
			point = unseen[0]

			if point not in seen:
				tile = self.game_state.level.tiles.get(str(point), Tile(Tile.VOID))

				if tile.attribute == Tile.ROOM_WALL:
					return point

				seen.append(point)
				unseen.pop(0)

				new_neighbors = point.neighbors()
				for neighbor in new_neighbors:
					if neighbor not in seen:
						unseen.append(neighbor)

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
				if neighbor_tile.attribute != Tile.VOID:
					if neighbor_tile.adversary == None:
						reachable_tiles.append(neighbor)
		
		return point in reachable_tiles
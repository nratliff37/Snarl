from abc import ABC, abstractmethod
from point import Point

#
# Represents an adversary
#
class Adversary(ABC):

	# Adversary types
	ZOMBIE = "zombie"
	GHOST = "ghost"
	
	def __init__(self, name, type):
		self.name = name
		self.location = None
		self.type = type
		self.game_state = None

	#
	# Returns how to render on the map
	# -> String
	#
	@abstractmethod
	def render(self):
		pass

	#
	# Called when the turn begins, returns the move to the game manager
	# GameState -> PointArr
	#
	@abstractmethod
	def begin_turn(self, state):
		pass

	#
	# The logic for each adversary type to move
	# -> Point
	#
	@abstractmethod
	def ai(self):
		pass

	#
	# Sends a point in the format of an array to the game manager
	# Point -> PointArr
	#
	@abstractmethod
	def send_message(self, point):
		pass
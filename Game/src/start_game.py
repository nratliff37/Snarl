from game_manager import GameManager
from level import Level
from point import Point

game_manager = GameManager()

game_manager.add_user("Vincent")
game_manager.add_observer()

level = Level()
level.add_room(Point(0,0), "xxxxx\nxooox\nxooox\nxooox\nxxxxx\n")
level.add_room(Point(7,0), "xxxxx\nxooox\nxooox\nxooox\nxxxxx\n")
player_locations = [Point(1,1)]
adversary_locations = [Point(2,2)]

game_manager.start_game(level, player_locations, adversary_locations, None, None)
from game_state import GameState
from point import Point
from player import Player
from adversary import Adversary
from zombie import Zombie

def test_initial_game_state(capfd):
    state = GameState()

    player_a = Player(0, "Harrison")
    player_b = Player(1, "Chris")
    state.add_player(player_a)
    state.add_player(player_b)

    assert len(state.players) == 2

    player_0 = state.players[0]
    player_1 = state.players[1]

    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]

    state.set_level(1, level_JSON)

    state.place_player(player_0, Point(1,1))
    state.place_player(player_1, Point(1,2))

    assert state.player_locations[0] == Point(1, 1)
    assert state.level.tiles["1,1"].player == player_0
    assert state.player_locations[1] == Point(1, 2)
    assert state.level.tiles["1,2"].player == player_1

    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    assert len(state.adversaries) == 1

    adversary = state.adversaries[0]
    state.place_adversary(adversary, Point(18, 4))

    assert state.adversary_locations["Jackson"] == Point(18, 4)
    assert state.level.tiles["18,4"].adversary == adversary


    state.level.render_map()
    out, err = capfd.readouterr()
    
    assert out == ("xxxxxx\n"
                   "xHCoox\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xxdxxx\n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "xxdxxx\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xoooZx\n"
                   "xoooox\n"
                   "xxxxxx\n\n")

def test_intermediate_game_state(capfd):
    state = GameState()

    player_a = Player(0, "Harrison")
    player_b = Player(1, "Chris")
    state.add_player(player_a)
    state.add_player(player_b)

    assert len(state.players) == 2

    player_0 = state.players[0]
    player_1 = state.players[1]

    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]

    state.set_level(1, level_JSON)

    state.place_player(player_0, Point(1,1))
    state.place_player(player_1, Point(1,2))

    assert state.player_locations[0] == Point(1, 1)
    assert state.level.tiles["1,1"].player == player_0
    assert state.player_locations[1] == Point(1, 2)
    assert state.level.tiles["1,2"].player == player_1

    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    assert len(state.adversaries) == 1

    adversary = state.adversaries[0]
    state.place_adversary(adversary, Point(18, 4))

    assert state.adversary_locations["Jackson"] == Point(18, 4)
    assert state.level.tiles["18,4"].adversary == adversary

    level = state.level

    level.place_key(Point(16, 2))
    state.move_player(player_0, Point(1,3))
    state.move_player(player_1, Point(3,2))
    state.move_adversary(adversary, Point(17, 4))

    state.level.render_map()
    out, err = capfd.readouterr()
    
    assert out == ("xxxxxx\n"
                   "xooHox\n"
                   "xoooox\n"
                   "xoCoox\n"
                   "xoooox\n"
                   "xxdxxx\n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "xxdxxx\n"
                   "xokoox\n"
                   "xoooZx\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xxxxxx\n\n")

    assert not state.key_found()

def test_obtained_item(capfd):
    state = GameState()

    player_a = Player(0, "Harrison")
    player_b = Player(1, "Chris")
    state.add_player(player_a)
    state.add_player(player_b)

    assert len(state.players) == 2

    player_0 = state.players[0]
    player_1 = state.players[1]

    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]

    state.set_level(1, level_JSON)

    state.place_player(player_0, Point(15,2))
    state.place_player(player_1, Point(16,4))

    assert state.player_locations[0] == Point(15, 2)
    assert state.level.tiles["15,2"].player == player_0
    assert state.player_locations[1] == Point(16, 4)
    assert state.level.tiles["16,4"].player == player_1

    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    assert len(state.adversaries) == 1

    adversary = state.adversaries[0]
    state.place_adversary(adversary, Point(18, 4))

    assert state.adversary_locations["Jackson"] == Point(18, 4)
    assert state.level.tiles["18,4"].adversary == adversary

    level = state.level

    level.place_key(Point(16, 2))
    
    state.move_player(player_0, Point(16, 2))
    state.interact_player(player_0)
    state.move_player(player_1, Point(17, 4))
    state.move_adversary(adversary, Point(17, 4))
    state.interact_adversary(adversary)

    state.move_player(player_0, Point (17, 2))
    state.move_adversary(adversary, Point(17, 3))

    level.render_map()
    out, err = capfd.readouterr()

    assert out == ("xxxxxx\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xxdxxx\n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "  f   \n"
                   "xxdxxx\n"
                   "xoooox\n"
                   "xoHZox\n"
                   "xoooox\n"
                   "xoooox\n"
                   "xxxxxx\n\n")

    assert player_0.status == Player.ALIVE
    assert player_1.status == Player.DEAD
    assert level.key_found
    assert state.level.tiles["17,2"].player == player_0
    assert state.level.tiles["17,3"].adversary == adversary
    assert state.player_locations[0] == Point(17, 2)
    assert state.adversary_locations["Jackson"] == Point(17, 3)

def test_add_player():
    state = GameState()
    player_a = Player(0, "Harrison")
    player_b = Player(1, "Chris")
    player_c = Player(2, "Harri")
    player_d = Player(3, "Christ")
    state.add_player(player_a)
    state.add_player(player_b)
    state.add_player(player_c)
    state.add_player(player_d)

    assert len(state.players) == 4

def test_add_adversary():
    state = GameState()
    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    assert len(state.adversaries) == 1

def test_key_found():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]

    state.set_level(1, level_JSON)
    assert state.key_found() == False
    state.level.key_found = True
    assert state.key_found() == True

def test_place_player():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    player_a = Player(0, "Harrison")
    state.add_player(player_a)
    player_0 = state.players[0]
    state.place_player(player_0, Point(15, 2))

    assert state.player_locations[0] == Point(15, 2)
    assert state.level.tiles["15,2"].player == player_0

def test_move_player():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    player_a = Player(0, "Harrison")
    state.add_player(player_a)
    player_0 = state.players[0]
    state.place_player(player_0, Point(15,2))

    assert state.player_locations[0] == Point(15, 2)
    assert state.level.tiles["15,2"].player == player_0
    
    state.move_player(player_0, Point(16, 2))
    assert state.player_locations[0] == Point(16, 2)
    assert state.level.tiles["16,2"].player == player_0

def test_place_adversary():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)
    adversary_0 = state.adversaries[0]
    state.place_adversary(adversary_0, Point(15, 2))

    assert state.adversary_locations["Jackson"] == Point(15, 2)
    assert state.level.tiles["15,2"].adversary == adversary_0

def test_move_adversary():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)
    adversary_0 = state.adversaries[0]
    state.place_adversary(adversary_0, Point(15, 2))

    assert state.adversary_locations["Jackson"] == Point(15, 2)
    assert state.level.tiles["15,2"].adversary == adversary_0
    
    state.move_adversary(adversary_0, Point(16, 2))
    assert state.adversary_locations["Jackson"] == Point(16, 2)
    assert state.level.tiles["16,2"].adversary == adversary_0

def test_set_level():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    

    assert state.current_level == 1
    assert state.level

def test_interact_item():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    
    player_a = Player(0, "Harrison")
    state.add_player(player_a)
    player_b = Player(1, "Chris")
    state.add_player(player_b)

    player_0 = state.players[0]
    state.place_player(player_0, Point(16, 2))
    player_1 = state.players[1]
    state.place_player(player_1, Point(17, 2))

    assert state.player_locations[0] == Point(16, 2)
    assert state.level.tiles["16,2"].player == player_0
    assert state.player_locations[1] == Point(17, 2)
    assert state.level.tiles["17,2"].player == player_1
    level = state.level

    level.place_key(Point(16, 2))
    state.interact_player(player_0)

    assert state.key_found() == True

    level.place_exit(Point(17, 2))
    state.interact_player(player_1)

    assert player_1.status == Player.EXITED

def test_interact_adversary():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    
    player_a = Player(0, "Harrison")
    state.add_player(player_a)
    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    player_0 = state.players[0]
    state.place_player(player_0, Point(16, 2))
    adversary_0 = state.adversaries[0]
    state.place_adversary(adversary_0, Point(16, 2))

    assert state.player_locations[0] == Point(16, 2)
    assert state.level.tiles["16,2"].player == player_0
    assert state.adversary_locations["Jackson"] == Point(16, 2)
    assert state.level.tiles["16,2"].adversary == adversary_0
    level = state.level

    state.interact_adversary(adversary_0)


    assert player_0.status == Player.DEAD

def test_interact_player():
    state = GameState()
    level_JSON = [{"type" : "room",
                   "origin" : [0, 0],
                   "bounds" : None,
                   "layout" : [ ["x", "x", "x", "x", "x", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "o", "o", "o", "o", "x"],
                                ["x", "x", "d", "x", "x", "x"]]},
                   {"type" : "room",
                    "origin" : [15, 0],
                    "bounds" : None,
                    "layout" : [ ["x", "x", "d", "x", "x", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "o", "o", "o", "o", "x"],
                                 ["x", "x", "x", "x", "x", "x"]]},
                   {"type" : "hallway",
                    "endpoint_1" : [5, 2],
                    "endpoint_2" : [15, 2],
                    "waypoints" : []
                   }
                  ]
    state.set_level(1, level_JSON)    
    
    player_a = Player(0, "Harrison")
    state.add_player(player_a)
    adversary_0 = Zombie("Jackson")
    state.add_adversary(adversary_0)

    player_0 = state.players[0]
    state.place_player(player_0, Point(16, 2))
    adversary_0 = state.adversaries[0]
    state.place_adversary(adversary_0, Point(16, 2))

    assert state.player_locations[0] == Point(16, 2)
    assert state.level.tiles["16,2"].player == player_0
    assert state.adversary_locations["Jackson"] == Point(16, 2)
    assert state.level.tiles["16,2"].adversary == adversary_0
    level = state.level

    state.interact_player(player_0)


    assert player_0.status == Player.DEAD



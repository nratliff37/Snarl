from  rulechecker import RuleChecker
from game_state import GameState
from player import Player
from point import Point

def test_validate_place_player():
    gs = GameState()
    p1 = Player(0, "Player 1")

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

    gs.set_level(1, level_JSON)
    gs.add_player(p1)

    rc = RuleChecker(gs)

    # Valid locations, including hallways and doors
    assert rc.validate_place_player(Point(3,3))
    assert rc.validate_place_player(Point(4,1))
    assert rc.validate_place_player(Point(7,2))
    assert rc.validate_place_player(Point(17,3))
    assert rc.validate_place_player(Point(19,4))
    assert rc.validate_place_player(Point(5,2))

    # Invlid locations
    assert not rc.validate_place_player(Point(0,0))
    assert not rc.validate_place_player(Point(2,10))
    assert not rc.validate_place_player(Point(7,3))
    assert not rc.validate_place_player(Point(11,4))
    assert not rc.validate_place_player(Point(20,3))
    assert not rc.validate_place_player(Point(18,7))

def test_validate_move_player():
    gs = GameState()
    p1 = Player(0, "Player 1")
    p1.location = Point(4, 1)

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

    gs.set_level(1, level_JSON)
    gs.add_player(p1)
    gs.place_player(p1, p1.location)

    rc = RuleChecker(gs)

    # Valid locations
    assert rc.validate_move_player(p1, Point(4, 2))
    assert rc.validate_move_player(p1, Point(5, 2))
    assert rc.validate_move_player(p1, Point(3, 2))

    # Invalid locations
    assert not rc.validate_move_player(p1, Point(0, 0))
    assert not rc.validate_move_player(p1, Point(1, 2))
    assert not rc.validate_move_player(p1, Point(3, 8))

    # Hallways
    p1.location = Point(11, 2)
    gs.place_player(p1, p1.location)

    # Valid
    assert rc.validate_move_player(p1, Point(10, 2))
    assert rc.validate_move_player(p1, Point(9, 2))
    assert rc.validate_move_player(p1, Point(12, 2))
    assert rc.validate_move_player(p1, Point(13, 2))

    # Invalid
    assert not rc.validate_move_player(p1, Point(8, 2))
    assert not rc.validate_move_player(p1, Point(14, 2))
    assert not rc.validate_move_player(p1, Point(11, 3))

def test_validate_move_player_onto_player():
    gs = GameState()
    p1 = Player(0, "Player 1")
    p1.location = Point(4, 1)
    p2 = Player(1, "Player 2")
    p2.location = Point(3, 1)

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

    gs.set_level(1, level_JSON)
    gs.add_player(p1)
    gs.place_player(p1, p1.location)
    gs.add_player(p2)
    gs.place_player(p2, p2.location)

    rc = RuleChecker(gs)

    assert rc.validate_move_player(p1, Point(2, 1))
    assert not rc.validate_move_player(p1, Point(3, 1))

def test_all_dead():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")

    p1.set_status(Player.DEAD)
    p2.set_status(Player.DEAD)

    gs.add_player(p1)
    gs.add_player(p2)

    rc = RuleChecker(gs)

    assert rc.all_dead()

def test_not_all_dead():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")

    p1.set_status(Player.DEAD)

    gs.add_player(p1)
    gs.add_player(p2)

    rc = RuleChecker(gs)

    assert not rc.all_dead()

def test_game_won_all_exit():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")
    p3 = Player(2, "Player 3")

    p1.set_status(Player.EXITED)
    p2.set_status(Player.EXITED)
    p3.set_status(Player.EXITED)

    gs.add_player(p1)
    gs.add_player(p2)
    gs.add_player(p3)

    rc = RuleChecker(gs)

    assert rc.game_won()

def test_game_won_one_exit():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")
    p3 = Player(2, "Player 3")

    p1.set_status(Player.DEAD)
    p2.set_status(Player.DEAD)
    p3.set_status(Player.EXITED)

    gs.add_player(p1)
    gs.add_player(p2)
    gs.add_player(p3)

    rc = RuleChecker(gs)

    assert rc.game_won()

def test_game_won_all_dead():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")
    p3 = Player(2, "Player 3")

    p1.set_status(Player.DEAD)
    p2.set_status(Player.DEAD)
    p3.set_status(Player.DEAD)

    gs.add_player(p1)
    gs.add_player(p2)
    gs.add_player(p3)

    rc = RuleChecker(gs)

    assert not rc.game_won()

# This tests the case where some players are still in the game
def test_game_won_remaining_players():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")
    p3 = Player(2, "Player 3")

    p1.set_status(Player.EXITED)
    p2.set_status(Player.ALIVE)
    p3.set_status(Player.ALIVE)

    gs.add_player(p1)
    gs.add_player(p2)
    gs.add_player(p3)

    rc = RuleChecker(gs)

    assert not rc.game_won()

# This tests the case where every player is still in the game
def test_game_won_all_alive():
    gs = GameState()

    p1 = Player(0, "Player 1")
    p2 = Player(1, "Player 2")
    p3 = Player(2, "Player 3")

    p1.set_status(Player.ALIVE)
    p2.set_status(Player.ALIVE)
    p3.set_status(Player.ALIVE)

    gs.add_player(p1)
    gs.add_player(p2)
    gs.add_player(p3)

    rc = RuleChecker(gs)

    assert not rc.game_won()
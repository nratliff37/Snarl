from level import Level
from point import Point
from game_manager import GameManager
from adversary import Adversary

LEVEL_JSON = [{"type" : "room",
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

def test_add_user():
    gm = GameManager(1, LEVEL_JSON)
    assert len(gm.users) == 0

    gm.add_user("Nick")
    assert len(gm.users) == 1

    gm.add_user("Vincent")
    assert len(gm.users) == 2

    # Check that attempting to add player with same name does not add the player
    gm.add_user("Nick")
    gm.add_user("Vincent")
    assert len(gm.users) == 2

    # Test that id's start at 0 and increase from when they were added
    nick = gm.users[0]
    assert nick.id == 0

    vincent = gm.users[1]
    assert vincent.id == 1

    # Add two more players and check that you can't add any past 4
    gm.add_user("Jackson")
    gm.add_user("Chris")
    assert len(gm.users) == 4

    gm.add_user("Harrison")
    assert len(gm.users) == 4

def test_add_adversary():
    gm = GameManager(1, LEVEL_JSON)
    assert len(gm.adversaries) == 0

    gm.add_adversary("Zombie 1", Adversary.ZOMBIE)
    assert len(gm.adversaries) == 1

    gm.add_adversary("Zombie 2", Adversary.ZOMBIE)
    assert len(gm.adversaries) == 2

    # Check that attempting to add adversary with same name does not add the adversary
    gm.add_adversary("Zombie 1", Adversary.ZOMBIE)
    gm.add_adversary("Zombie 2", Adversary.ZOMBIE)
    assert len(gm.adversaries) == 2

    # Test that we can add more than 4 adversaries
    gm.add_adversary("Ghost 1", Adversary.GHOST)
    gm.add_adversary("Ghost 2", Adversary.GHOST)
    gm.add_adversary("Zombie 3", Adversary.ZOMBIE)
    gm.add_adversary("Ghost 3", Adversary.GHOST)
    assert len(gm.adversaries) == 6

def test_set_level():
    gm = GameManager(1, LEVEL_JSON)

    l = Level()
    l.add_room(Point(0,0), ("xxxxxx\n"
                            "xoooox\n"
                            "xoooox\n"
                            "xxxxxx\n"))

    gm.set_level(l)
    assert gm.game_state.level == l
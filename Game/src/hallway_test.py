from point import Point
from tile import Tile
from hallway import Hallway

def test_generate_key():
    hallway = Hallway(Point(0,0), Point(1,1), [Point(0,1)])

    x = 4
    y = 9

    key = hallway.generate_key(x, y)

    assert key == "4,9"

def test_tiles():
    hallway = Hallway(Point(0,0), Point(1,1), [Point(0,1)])

    assert hallway.tiles["0,0"].attribute == Tile.DOOR
    assert hallway.tiles["1,1"].attribute == Tile.DOOR

    assert hallway.tiles["0,1"].attribute == Tile.HALLWAY_FLOOR


def test_tiles_no_waypoints():
    hallway = Hallway(Point(0,0), Point(0,2), [])

    assert hallway.tiles["0,0"].attribute == Tile.DOOR
    assert hallway.tiles["0,2"].attribute == Tile.DOOR

    assert hallway.tiles["0,1"].attribute == Tile.HALLWAY_FLOOR


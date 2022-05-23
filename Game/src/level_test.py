from level import Level
from point import Point
from tile import Tile

def test_add_room():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")

    assert "0,0" in level.rooms

def test_overlap_room():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")
    level.add_room(Point(1,1), "xxx\nxox\nxxx")

    assert "0,0" in level.rooms
    assert "1,1" not in level.rooms


def test_two_rooms():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")
    level.add_room(Point(4,4), "xxx\nxox\nxxx")

    assert "0,0" in level.rooms
    assert "4,4" in level.rooms

def test_add_hallway():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxod\nxxx")
    level.add_room(Point(4,5), "xdx\nxox\nxxx")
    level.add_hallway(Point(1,2), Point(4,6), [Point(1,6)])

    assert "1,2 4,6" in level.hallways

def test_next_to_each_other_hallway():
    level = Level()
    level.add_room(Point(0,0), "xxd\nxod\nxxx")
    level.add_room(Point(4,5), "xdd\nxox\nxxx")
    level.add_hallway(Point(1,2), Point(4,6), [Point(1,6)])
    level.add_hallway(Point(0,2), Point(4,7), [Point(0,7)])
    
    assert "1,2 4,6" in level.hallways
  
    assert "1,2 4,6" in level.hallways
    assert "0,2 4,7" in level.hallways

def test_overlap_hallway():
    level = Level()
    level.add_room(Point(0,0), "xxd\nxod\nxxx")
    level.add_room(Point(4,5), "xdd\nxox\nxxx")
    level.add_hallway(Point(1,2), Point(4,6), [Point(1,6)])
    level.add_hallway(Point(0,2), Point(4,5), [Point(0,5)])
    
    assert "1,2 4,6" in level.hallways
  
    assert "1,2 4,6" in level.hallways
    assert "0,2 4,5" not in level.hallways

def test_two_hallways():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxod\nxdx")
    level.add_room(Point(4,4), "xdx\ndox\nxxx")

    level.add_hallway(Point(1,2), Point(4,5), [Point(1,5)])
    level.add_hallway(Point(2,1), Point(5,4), [Point(5,1)])
    
    assert "1,2 4,5" in level.hallways
    assert "2,1 5,4" in level.hallways

def test_place_key():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")
    level.place_key(Point(1, 1))
    assert level.tiles["1,1"].render() == Tile.KEY

def test_place_exit():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")
    level.place_exit(Point(1, 1))
    assert level.tiles["1,1"].render() == Tile.EXIT

def test_get_corners():
    level = Level()
    level.add_room(Point(0,0), "xxx\nxox\nxxx")

    assert level.get_corners() == {
            "smallest_x": 0,
            "biggest_x": 2,
            "smallest_y": 0,
            "biggest_y": 2
        }

    level.add_room(Point(4,4), "xxx\nxox\nxxx")

    assert level.get_corners() == {
            "smallest_x": 0,
            "biggest_x": 6,
            "smallest_y": 0,
            "biggest_y": 6
        }

def test_render_map(capfd):

    level = Level()
    level.add_room(Point(0,0), "xxx\nxod\nxxx")
    level.add_room(Point(4,5), "xdx\nxox\nxxx")
    level.add_hallway(Point(1,2), Point(4,6), [Point(1,6)])

    level.render_map()

    out, err = capfd.readouterr()
    
    assert out == ("xxx     \n"
                   "xodffff \n"
                   "xxx   f \n"
                   "      f \n"
                   "     xdx\n"
                   "     xox\n"
                   "     xxx\n\n")

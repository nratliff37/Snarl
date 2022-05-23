from tile import *
from room import *
from point import *

def test_valid_room():
    room = Room(Point(0,0), "xxx\nxox\nxxx")
    valid = room.validate_layout("xxx\nxox\nxxx")

    assert valid == True

def test_valid_room_door():
    room = Room(Point(0,0), "xxx\nxox\nxdx")
    valid = room.validate_layout("xxx\nxox\nxdx")

    assert valid == True

def test_invalid_no_floor():
    room = Room(Point(0,0), "xxx\nxxx\nxxx")
    valid = room.validate_layout("xxx\nxxx\nxxx")

    assert valid == False

def test_invalid_open_wall():
    room = Room(Point(0,0), "xox\nxxx\nxxx")
    valid = room.validate_layout("xox\nxxx\nxxx")

    assert valid == False

def test_invalid_open_corner():
    room = Room(Point(0,0), "xxx\nxxx\noxx")
    valid = room.validate_layout("xxx\nxxx\noxx")

    assert valid == False

def test_invalid_too_small():
    room = Room(Point(0,0), "xx\nxx")
    valid = room.validate_layout("xx\nxx")

    assert valid == False

def test_invalid_not_rectangle():
    room = Room(Point(0,0), "xxxxx\nxoox\nxox\nxx\nx")
    valid = room.validate_layout("xxxxx\nxoox\nxox\nxx\nx")

    assert valid == False

def test_invalid_wrong_characters():
    room = Room(Point(0,0), "My\nname\nis\nNick\nRatliff")
    valid = room.validate_layout("My\nname\nis\nNick\nRatliff")

    assert valid == False

def test_valid_new_origin():
    room = Room(Point(2,5), "xxxxx\nxooxx\nxooox\nxxxxx")
    valid = room.validate_layout("xxxxx\nxooxx\nxooox\nxxxxx")

    assert valid == True

def test_initialize_tiles():
    room = Room(Point(0,0), "xxx\nxox\nxxx")
    room.initialize_tiles("xxx\nxox\nxxx")

    assert room.tiles["0,0"].attribute == Tile.ROOM_WALL
    assert room.tiles["1,0"].attribute == Tile.ROOM_WALL
    assert room.tiles["2,0"].attribute == Tile.ROOM_WALL
    assert room.tiles["0,1"].attribute == Tile.ROOM_WALL
    assert room.tiles["1,1"].attribute == Tile.ROOM_FLOOR
    assert room.tiles["2,1"].attribute == Tile.ROOM_WALL
    assert room.tiles["0,2"].attribute == Tile.ROOM_WALL
    assert room.tiles["1,2"].attribute == Tile.ROOM_WALL
    assert room.tiles["2,2"].attribute == Tile.ROOM_WALL

def test_generate_key():
    room = Room(Point(0,0), "xxx\nxox\nxxx")

    x = 2
    y = 3

    key = room.generate_key(x, y)

    assert key == "2,3"
from tile import Tile

def test_place_exit():
    tile = Tile(Tile.ROOM_FLOOR)
    tile.place_exit()

    assert tile.item == Tile.EXIT

def test_place_key():
    tile = Tile(Tile.ROOM_FLOOR)
    tile.place_key()

    assert tile.item == Tile.KEY

def test_render_room_wall():
    tile = Tile(Tile.ROOM_WALL)
    render = tile.render()

    assert render == "x"

def test_render_room_floor():
    tile = Tile(Tile.ROOM_FLOOR)
    render = tile.render()

    assert render == "o"

def test_render_door():
    tile = Tile(Tile.DOOR)
    render = tile.render()

    assert render == "d"

def test_render_hallway_floor():
    tile = Tile(Tile.HALLWAY_FLOOR)
    render = tile.render()

    assert render == "f"
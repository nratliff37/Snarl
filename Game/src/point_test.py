from point import *

def test_horizontal_going_right_neighbors():
    this_point = Point(2, 3)
    other_point = Point(6, 3)

    neighbors = this_point.get_intermediate_points(other_point)

    assert neighbors[0].x == 2
    assert neighbors[0].y == 3

    assert neighbors[1].x == 3
    assert neighbors[1].y == 3

    assert neighbors[2].x == 4
    assert neighbors[2].y == 3

    assert neighbors[3].x == 5
    assert neighbors[3].y == 3

def test_horizontal_going_left_neighbors():
    this_point = Point(6, 3)
    other_point = Point(2, 3)

    neighbors = this_point.get_intermediate_points(other_point)

    assert neighbors[0].x == 6
    assert neighbors[0].y == 3

    assert neighbors[1].x == 5
    assert neighbors[1].y == 3

    assert neighbors[2].x == 4
    assert neighbors[2].y == 3

    assert neighbors[3].x == 3
    assert neighbors[3].y == 3

def test_vertical_going_down_neighbors():
    this_point = Point(3, 2)
    other_point = Point(3, 7)

    neighbors = this_point.get_intermediate_points(other_point)

    assert neighbors[0].x == 3
    assert neighbors[0].y == 2

    assert neighbors[1].x == 3
    assert neighbors[1].y == 3

    assert neighbors[2].x == 3
    assert neighbors[2].y == 4

    assert neighbors[3].x == 3
    assert neighbors[3].y == 5

    assert neighbors[4].x == 3
    assert neighbors[4].y == 6

def test_vertical_going_up_neighbors():
    this_point = Point(3, 7)
    other_point = Point(3, 2)

    neighbors = this_point.get_intermediate_points(other_point)

    assert neighbors[0].x == 3
    assert neighbors[0].y == 7

    assert neighbors[1].x == 3
    assert neighbors[1].y == 6

    assert neighbors[2].x == 3
    assert neighbors[2].y == 5

    assert neighbors[3].x == 3
    assert neighbors[3].y == 4

    assert neighbors[4].x == 3
    assert neighbors[4].y == 3

def test_neighbors():
    point = Point(4, 5)

    neighbors = point.neighbors();

    assert neighbors[0].x == 4
    assert neighbors[0].y == 4

    assert neighbors[1].x == 5
    assert neighbors[1].y == 5

    assert neighbors[2].x == 3
    assert neighbors[2].y == 5

    assert neighbors[3].x == 4
    assert neighbors[3].y == 6

def test_string():
    point = Point(6, 9)

    string = str(point)

    assert string == "6,9"
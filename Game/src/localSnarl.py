#!/usr/bin/python3

# DEPRECATED, ONLY NETWORKED VERSION WORKS NOW 


import argparse
import json
import sys
sys.path.insert(0, "./src")
from game_manager import GameManager

parser = argparse.ArgumentParser()
parser.add_argument("--levels", type=str, default="snarl.levels")
parser.add_argument("--players", type=int, default=1)
parser.add_argument("--start", type=int, default=1)
parser.add_argument("--observe", action="store_true")

args = parser.parse_args()

if args.players > 4 or args.players < 1:
    print("Total players must be between 1 and 4")
    exit()


def is_json(maybe_json_string):
    try:
        json_object = json.loads(maybe_json_string)
    except ValueError as e:
        return False
    return True

game_file = open(args.levels, "r")

num_levels = int(game_file.readline())

level_array = []
for i in range (num_levels):
    json_loads = False
    json_string = ""
    level_json = None

    while not json_loads:
        next_line = game_file.readline()
        json_string = json_string + next_line

        if is_json(json_string):
            level_json = json.loads(json_string)
            json_loads = True

    level_array.append(level_json)

gm = GameManager(num_levels, level_array)

for i in range (args.players):
    name = input("Enter username for Player " + str(i + 1) + ": ")
    gm.add_user(name)


gm.start_game(args.start)

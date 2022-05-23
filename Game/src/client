#!/usr/bin/python3

import argparse
import json
import sys
import re
sys.path.insert(0, "./src")
import socket
from point import Point
from player import Player
from tile import Tile
from zombie import Zombie
from ghost import Ghost


parser = argparse.ArgumentParser()
parser.add_argument("--address", type=str, default="127.0.0.1")
parser.add_argument("--port", type=int, default="45678")

args = parser.parse_args()


server_socket = socket.socket()
current_tiles = {}
current_position = None

def is_json(maybe_json_string):
    try:
        json_object = json.loads(maybe_json_string)
    except ValueError as e:
        return False
    return True

def parse_response(response):
    new = ""
    for char in response:
        if char == "\"" or char == "}":
            new = new + char + "\n"
        else:
            new = new + char 
    response_arr = new.split("\n")

    instructions = []
    json_obj = ""
    for line in response_arr:
        json_obj = json_obj + line
        if is_json(json_obj):
            complete_obj = json.loads(json_obj)
            instructions.append(complete_obj)
            json_obj = ""
        else:
            continue
    return instructions


def generate_tiles(position, tiles, actors, items):
    top_left_x = position[0] - 2
    top_left_y = position[1] - 2

    for i in range(5):
        for j in range(5):
            tile = tiles[i].pop(0)
            x = top_left_x + i
            y = top_left_y + j
            key = str(x) + "," + str(y)

            if tile == 0:
                current_tiles[key] = Tile(Tile.ROOM_WALL)
            elif tile == 1:
                current_tiles[key] = Tile(Tile.ROOM_FLOOR)
            elif tile == 2:
                current_tiles[key] = Tile(Tile.DOOR)
    for actor in actors:
        key = str(actor["position"][0]) + "," + str(actor["position"][1])
        if actor["type"] == "player":
            current_tiles[key].place_player(Player(0, actor["name"]))
        elif actor["type"] == "zombie":
            current_tiles[key].place_adversary(Zombie(actor["name"]))
        elif actor["type"] == "ghost":
            current_tiles[key].place_adversary(Ghost(actor["name"]))
    
    for item in items:
        key = str(item["position"][0]) + "," + str(item["position"][1])
        if item["type"] == "key":
            current_tiles[key].place_key()
        elif item["type"] == "exit":
            current_tiles[key].place_exit()


def render(position):
    map = ""

    top_left_x = position[0] - 2
    top_left_y = position[1] - 2
    
    for i in range(5):
        for j in range(5):
            x = top_left_x + i
            y = top_left_y + j
            key = str(x) + "," + str(y)

            map = map + current_tiles[key].render()
        map = map + "\n"
    
    print(map)

try:
    server_socket.connect((args.address, args.port))
except socket.error as e:
    print(str(e))

# Server Welcome
resp = server_socket.recv(1024)
print(resp)
    
# name
resp = server_socket.recv(1024)
print(resp)
   
username = input('Enter your username here: ')
server_socket.send(str.encode(username))
    
while True:
        
    resp = server_socket.recv(1024)
    
    response = resp.decode()
    instructions = parse_response(response)
    
    for obj in instructions:
        if obj == "move":
            print("Current position: " + str(current_position))
            move = input("Enter your move here: ")

            if re.match(r'^[0-9]+,[0-9]+', move):
                move_arr = move.split(",")
                move_response = {
                    "type": "move",
                    "to": move_arr
                }
            else:
                move_response = {
                    "type": "move",
                    "to": current_position
                }
            server_socket.send(json.dumps(move_response).encode())
            result = server_socket.recv(1024)
            print(result.decode())
        else:
            typ = obj["type"]
            if typ == "start-level":
                print("Level " + str(obj["level"]))
            elif typ == "player-update":
                tiles = obj["layout"]
                position = obj["position"]
                current_position = position
                actors = obj["actors"]
                objects = obj["objects"]
                generate_tiles(position, tiles, actors, objects)
                print('---------------------------')
                render(position)
            elif typ == "end-level":
                print("Level Over")
            elif typ == "end-game":
                print("Game Over")
                for score in obj["scores"]:
                    print('---------------------------')
                    print(score["name"])
                    print("Times exited: " + str(score["exits"]))
                    print("Times ejected: " + str(score["ejects"]))
                    print("Times found key: " + str(score["keys"]))
                server_socket.close()
                exit()
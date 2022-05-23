#!/usr/bin/python3

import socket
import os
from _thread import *
import argparse
import json
import sys
sys.path.insert(0, "./src")
from game_manager import GameManager

parser = argparse.ArgumentParser()
parser.add_argument("--levels", type=str, default="snarl.levels")
parser.add_argument("--clients", type=int, default=4)
parser.add_argument("--wait", type=int, default=60)
parser.add_argument("--observe", action="store_true")
parser.add_argument("--address", type=str, default="127.0.0.1")
parser.add_argument("--port", type=int, default="45678")

args = parser.parse_args()

timeout = 0

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

if args.observe:
    gm.add_observer()

server_socket = socket.socket()
server_socket.settimeout(args.wait)
host = args.address
port = args.port
connected_client_count = 0
user_sockets = {}

try:
    server_socket.bind((host, port))
except socket.error as e:
    print(str(e))

server_socket.listen(args.clients)

def handle_reply(message):
    return message

def client_thread(conn):
    print(conn)
    user_registered = False
    server_welcome = {
        "type": "welcome",
        "info": "Esseallond Server 1.0\nInvalid moves will result in a skipped turn"
    }
    conn.send(json.dumps(server_welcome).encode())
    conn.send(json.dumps("name").encode())
    while not user_registered:
        data = conn.recv(2048)
        username = data.decode()
        gm.add_network_user(username, conn)
        user_registered = True
        user_sockets[username] = conn
        



while connected_client_count < args.clients:
    try:
        client, address = server_socket.accept()
    except socket.timeout:
        exit()
    start_new_thread(client_thread, (client, ))
    connected_client_count += 1
    print("Player " + str(connected_client_count - 1) +  " has connected")



while len(gm.users) != args.clients:
    continue

if len(gm.users) == args.clients:
    server_socket.settimeout(None)
    gm.start_game(1)

for key, client in user_sockets.items():
    client.close() 

server_socket.close()

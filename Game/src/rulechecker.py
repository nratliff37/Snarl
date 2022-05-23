from tile import Tile
from player import Player
from adversary import Adversary

class RuleChecker:

    def __init__(self, game_state):
        self.game_state = game_state

    #
    # Return whether or not the placement of the given player is legal
    # Point -> boolean
    #
    def validate_place_player(self, point):
        try:
            tile = self.game_state.level.tiles[str(point)]
            tile_type = tile.attribute
            return (tile_type == Tile.ROOM_FLOOR or tile_type == Tile.HALLWAY_FLOOR or tile_type == Tile.DOOR) and tile.player == None
        except:
            return False
            
    #
    # Return whether or not the placement of the given adversary is legal
    # Point -> boolean
    #
    def validate_place_adversary(self, point):
        try:
            tile = self.game_state.level.tiles[str(point)]
            tile_type = tile.attribute
            return (tile_type == Tile.ROOM_FLOOR or tile_type == Tile.HALLWAY_FLOOR or tile_type == Tile.DOOR) and tile.adversary == None
        except:
            return False


    #
    # Return whether or not the given player can move to the given point
    # Player, Point -> boolean
    #
    def validate_move_player(self, player, point):
        to_tile = None
        try:
            to_tile = self.game_state.level.tiles[str(point)]
        except:
            return False

        to_tile_type = to_tile.attribute 

        from_tile = self.game_state.level.tiles[str(player.location)]

        neighbors = player.location.neighbors()
        reachable_tiles = [player.location]

        for neighbor in neighbors:
            neighbor_tile = self.game_state.level.tiles.get(str(neighbor), False)
            if neighbor_tile:
                if neighbor_tile.attribute == Tile.ROOM_FLOOR or neighbor_tile.attribute == Tile.HALLWAY_FLOOR or neighbor_tile.attribute == Tile.DOOR:
                    if neighbor_tile.player == None:
                        reachable_tiles.append(neighbor)
                    neighbors_2 = neighbor.neighbors()
                    for neighbor_2 in neighbors_2:
                        neighbor_2_tile = self.game_state.level.tiles.get(str(neighbor_2), False)
                        if neighbor_2_tile:
                            if neighbor_2_tile.attribute == Tile.ROOM_FLOOR or neighbor_2_tile.attribute == Tile.HALLWAY_FLOOR or neighbor_2_tile.attribute == Tile.DOOR:
                                if neighbor_2 not in reachable_tiles:
                                    if neighbor_2_tile.player == None:
                                        reachable_tiles.append(neighbor_2)

        return point in reachable_tiles
    
    #
    # Return whether or not the given adversary can move to the given point
    # Adversary, Point -> boolean
    #
    def validate_move_adversary(self, adversary, point):
        to_tile = None
        try:
            to_tile = self.game_state.level.tiles[str(point)]
        except:
            return False
        
        neighbors = adversary.location.neighbors()
        reachable_tiles = [adversary.location]

        for neighbor in neighbors:
            neighbor_tile = self.game_state.level.tiles.get(str(neighbor), False)
            if neighbor_tile:
                if adversary.type == Adversary.ZOMBIE:
                    if neighbor_tile.attribute == Tile.ROOM_FLOOR:
                        if neighbor_tile.adversary == None:
                            reachable_tiles.append(neighbor)
                elif adversary.type == Adversary.GHOST:
                    if neighbor_tile.attribute != Tile.VOID:
                        if neighbor_tile.adversary == None:
                            reachable_tiles.append(neighbor)
        
        return point in reachable_tiles
    #
    # Determines if all of the players are dead
    # -> boolean
    #
    def all_dead(self):
        all_dead = True
        for player in self.game_state.players:
            all_dead = all_dead and (player.status == Player.DEAD)

        return all_dead

    #
    # Determines if the players have won
    # -> boolean
    #
    def game_won(self):
        # Check that at least one person exited
        statuses = []
        for player in self.game_state.players:
            statuses.append(player.status)

        return Player.EXITED in statuses and Player.ALIVE not in statuses
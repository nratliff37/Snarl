from observer_client import ObserverClient

class Observer(ObserverClient):

    def __init__(self):
        self.game_state = None

    #
    # Updates the local game state to render
    # GameState -> void
    #
    def update(self, game_state):
        self.game_state = game_state
        self.render()

    # 
    # Renders the local game state
    # -> void
    #
    def render(self):
        self.game_state.level.render_map()
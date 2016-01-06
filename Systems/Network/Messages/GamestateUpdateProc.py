from Systems.Network.Messages.JsonProc import JsonProc
from Systems.Game.GameState import GameState
from Systems.Game.BallState import BallState
from Systems.Game.PlayerState import PlayerState
from Systems.Utils.JsonHelper import *


class GameStateUpdateProc(JsonProc):
    def __init__(self, game_state):
        super().__init__("game_state_update")
        self.data = dict()
        self.data['game_state'] = game_state

    def to_json(self):
        return to_json(self)

    def from_json(self, json_data):
        super().from_json(json_data)

        p1_json = json_data['data']['game_state']['player1']
        p2_json = json_data['data']['game_state']['player2']
        b_json = json_data['data']['game_state']['ball']

        p1 = PlayerState(float(p1_json['x']), float(p1_json['y']), int(p1_json['pts']))
        p2 = PlayerState(float(p2_json['x']), float(p2_json['y']), int(p2_json['pts']))
        b = BallState(float(b_json['x']), float(b_json['y']), float(b_json['vx']), float(b_json['vy']))

        self.data['game_state'] = GameState(data=(p1, p2, b))
        return self

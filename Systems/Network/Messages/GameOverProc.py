from Systems.Network.Messages.JsonProc import JsonProc
from Systems.Utils.JsonHelper import *


class GameOverProc(JsonProc):
    def __init__(self, result):
        super().__init__("game_over")
        self.data = dict()
        self.data['result'] = result

    def to_json(self):
        return to_json(self)

    def from_json(self, json_data):
        super().from_json(json_data)
        self.data['result'] = int(json_data['data']['result'])
        return self

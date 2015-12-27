from src.JsonHelper import from_json, to_json


class GameState:
    class PlayerData:
        def __init__(self, _id, _x, _y, _p):
            self.id = _id
            self.x = _x
            self.y = _y
            self.p = _p

    def __init__(self, players=None, json_val=None):
        if players:
            self.data = [players[0], players[1]]
        elif json_val:
            self.__dict__ = from_json(json_val)
        else:
            raise RuntimeError

    def to_json(self):
        return to_json(self)

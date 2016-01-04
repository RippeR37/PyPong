from Systems.Game.PlayerState import PlayerState
from Systems.Game.BallState import BallState
from Systems.Game.GameState import GameState


p1 = PlayerState(-1.0, 2.0)
p2 = PlayerState(-1.0, 2.0)
b = BallState(0.0, 0.0, 1.0, -1.0)

gs1 = GameState(data=(p1, p2, b))
gs2 = GameState(json_data=gs1.to_json())

print("GS1: {}".format(gs1.to_json()))
print("GS2: {}".format(gs2.to_json()))

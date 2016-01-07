from Systems.Game.PlayerState import PlayerState
from Systems.Game.BallState import BallState

class GameState(object):
    def __init__(self, data=None):
        self.player1 = None
        self.player2 = None
        self.ball = None

        if data:
            self.player1, self.player2, self.ball = data[0], data[1], data[2]
            assert isinstance(self.player1, PlayerState), "Player1 data must be of PlayerState type!"
            assert isinstance(self.player2, PlayerState), "Player2 data must be of PlayerState type!"
            assert isinstance(self.ball, BallState), "Ball data must be of BallState type!"
        else:
            self.player1 = PlayerState(-1.0, 0.0, 0)
            self.player2 = PlayerState(1.0, 0.0, 0)
            self.ball = BallState(0.0, 0.0, 0.0, 0.0)


class BallState(object):
    def __init__(self, _x, _y, _vx, _vy):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy

    def reset(self):
        self.x = self.y = self.vx = self.vy = 0.0

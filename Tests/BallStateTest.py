from Systems.Game.BallState import BallState
import unittest


class BallStateTest(unittest.TestCase):

    def test_constructor(self):
        x, vx = 32.52, 42.657
        y, vy = 85.21, 64.793
        bs = BallState(x, y, vx, vy)

        self.assertEqual(x, bs.x)
        self.assertEqual(y, bs.y)
        self.assertEqual(vx, bs.vx)
        self.assertEqual(vy, bs.vy)

    def test_reset(self):
        x, vx = 32.52, 42.657
        y, vy = 85.21, 64.793
        bs = BallState(x, y, vx, vy)

        bs.reset()

        self.assertEqual(0.0, bs.x)
        self.assertEqual(0.0, bs.y)
        self.assertEqual(0.0, bs.vx)
        self.assertEqual(0.0, bs.vy)

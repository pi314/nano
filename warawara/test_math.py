from .test_utils import *

import warawara as wara


class TestMath(TestCase):
    def test_sgn(self):
        sgn = wara.sgn
        self.eq(sgn(2024), 1)
        self.eq(sgn(0), 0)
        self.eq(sgn(-2024), -1)

    def test_lerp(self):
        lerp = wara.lerp
        self.eq(lerp(0, 10, 0.5), 5)
        self.eq(lerp(0, 9, 0.333333333333333333), 3)
        self.eq(lerp(-10, 10, 0), -10)
        self.eq(lerp(-10, 10, 0.1), -8)
        self.eq(lerp(-10, 10, 0.5), 0)
        self.eq(lerp(-10, 10, 1), 10)

    def test_clamp(self):
        clamp = wara.clamp
        self.eq(clamp(3, 0, 7), 3)
        self.eq(clamp(3, 5, 7), 5)
        self.eq(clamp(3, 9, 7), 7)

        with self.assertRaises(ValueError):
            clamp(7, 5, 3)

    def test_vector(self):
        vector = wara.vector
        v1 = vector(1, 2, 3)
        v2 = vector([4, 5, 6])

        self.eq(v1, vector(v1))

        self.eq(v1 + 2, (3, 4, 5))
        self.eq(2 + v1, (3, 4, 5))
        self.eq(v1 + v2, (5, 7, 9))
        self.eq(v1 + (4, 5, 6), (5, 7, 9))

        self.eq(v1 - 2, (-1, 0, 1))
        self.eq(v1 - v2, (-3, -3, -3))
        self.eq(v1 - (4, 5, 6), (-3, -3, -3))

        self.eq(v1 * 2, (2, 4, 6))
        self.eq(2 * v1, (2, 4, 6))
        self.eq(v1 * (4, 5, 6), (4, 10, 18))

        self.eq(v1 / 2, (0.5, 1.0, 1.5))
        self.eq(v1 // 2, (0, 1, 1))

        with self.assertRaises(TypeError):
            v1 / v2

        with self.assertRaises(TypeError):
            v1 // v2

        self.eq(v1.map(lambda x: x * 10), (10, 20, 30))

        with self.assertRaises(ValueError):
            vector('bla')

        with self.assertRaises(TypeError):
            vector(1, 2, 3) == 'bla'

        repr(v1)

        with self.assertRaises(ValueError):
            v1 + (1, 2, 3, 4)

        with self.assertRaises(ValueError):
            v1 - (1, 2, 3, 4)

        with self.assertRaises(ValueError):
            v1 * (1, 2, 3, 4)

        lerp = wara.lerp
        self.eq(lerp(v1, v2, 0), v1)
        self.eq(lerp(v1, v2, 0.5), (2.5, 3.5, 4.5))
        self.eq(lerp(v1, v2, 1), v2)
        self.eq(lerp(v1, v2, 2), (7, 8, 9))

    def test_interval(self):
        interval = wara.interval
        self.eq(list(interval(1, 3)), [1, 2, 3])
        self.eq(list(interval(3, 1)), [3, 2, 1])
        self.eq(list(interval(3, -3)), [3, 2, 1, 0, -1, -2, -3])
        self.eq(list(interval(3, -3, close=False)), [2, 1, 0, -1, -2])

        self.eq(list(interval(3, 3)), [3])
        self.eq(list(interval(3, 3, close=False)), [])

from typing import Iterable, Union


class Vec2d:
    def __init__(self, x: int, y: int = None):
        self.x = x
        self.y = y
        if y is None:
            self.y = x

    def __sub__(self, other: Union[int, float, 'Vec2d']):
        x, y = self.x, self.y
        if isinstance(other, int) or isinstance(other, float):
            x -= other
            y -= other
        else:
            x -= other.x
            y -= other.y
        return Vec2d(x, y)

    def __add__(self, other: Union[int, float, 'Vec2d']):
        x, y = self.x, self.y
        if isinstance(other, int) or isinstance(other, float):
            x += other
            y += other
        else:
            x += other.x
            y += other.y
        return Vec2d(x, y)

    def __truediv__(self, other: Union[int, float, 'Vec2d']):
        x, y = self.x, self.y
        if isinstance(other, int) or isinstance(other, float):
            x /= other
            y /= other
        else:
            x /= other.x
            y /= other.y
        return Vec2d(x, y)

    def __mul__(self, other: Union[int, float, 'Vec2d']):
        x, y = self.x, self.y
        if isinstance(other, int) or isinstance(other, float):
            x *= other
            y *= other
        else:
            x *= other.x
            y *= other.y
        return Vec2d(x, y)

    def __eq__(self, other: 'Vec2d'):
        return int(self.x) == int(other.x) and int(self.y) == int(other.y)

    def mag(self):
        return (self.x**2 + self.y**2) ** 0.5

    @classmethod
    def from_list(cls, pos: Iterable):
        x, y = pos
        return Vec2d(x, y)

    def norm(self):
        mag = max(self.mag(), 1)
        self.x /= mag
        self.y /= mag


def dist(vec1: Vec2d, vec2: Vec2d):
    return ((vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2)**0.5


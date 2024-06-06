from typing import Iterable, Union


class Vec2d:
    def __init__(self, x: float, y: float = None):
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

    def int(self):
        return Vec3d(int(self.x), int(self.y))

    def to_list(self):
        return [self.x, self.y]


class Vec3d:
    def __init__(self, x: float, y: float = None, z: float = None):
        self.x = x
        self.y = y
        if y is None and z is not None:
            raise ValueError("you set z, but not y")
        if y is None:
            self.y = x
        self.z = z if z is not None else x

    def __sub__(self, other: Union[int, float, 'Vec3d']):
        if isinstance(other, (int, float)):
            return Vec3d(self.x - other, self.y - other, self.z - other)
        return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Union[int, float, 'Vec3d']):
        if isinstance(other, (int, float)):
            return Vec3d(self.x + other, self.y + other, self.z + other)
        return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __truediv__(self, other: Union[int, float, 'Vec3d']):
        if isinstance(other, (int, float)):
            return Vec3d(self.x / other, self.y / other, self.z / other)
        return Vec3d(self.x / other.x, self.y / other.y, self.z / other.z)

    def __mul__(self, other: Union[int, float, 'Vec3d']):
        if isinstance(other, (int, float)):
            return Vec3d(self.x * other, self.y * other, self.z * other)
        return Vec3d(self.x * other.x, self.y * other.y, self.z * other.z)

    def __eq__(self, other: 'Vec3d'):
        return int(self.x) == int(other.x) and int(self.y) == int(other.y) and int(self.z) == int(other.z)

    def mag(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @classmethod
    def from_list(cls, pos: Iterable):
        x, y, z = pos
        return cls(x, y, z)

    def norm(self):
        mag = self.mag()
        if mag != 0:
            self.x /= mag
            self.y /= mag
            self.z /= mag
        return self

    def int(self):
        return Vec3d(int(self.x), int(self.y), int(self.z))

    def to_list(self):
        return [self.x, self.y, self.z]


def dist(vec1: Vec2d, vec2: Vec2d):
    return ((vec1.x-vec2.x)**2 + (vec1.y-vec2.y)**2)**0.5


def dist3d(vec1: Vec3d, vec2: Vec3d):
    return ((vec1.x - vec2.x) ** 2 + (vec1.y - vec2.y) ** 2 + (vec1.z - vec2.z) ** 2) ** 0.5


import functools
import math
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Sequence

sign = functools.partial(math.copysign, 1)

input = Path("input/day24.txt").read_text().strip().splitlines()

TEST_DATA = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""".splitlines()

EXPECTED = 2
TEST_MIN = 7
TEST_MAX = 27


def t_range(x: int, v: int, mn: int, mx: int) -> tuple[int, int]:
    t0 = max(0, (mn - x) / v)
    t1 = max(t0, (mx - x) / v)
    return t0, t1


def line_intersection(
    a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int]
) -> tuple[int, int] | None:
    q = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
    if q == 0:
        return None
    tq = (a[0] - c[0]) * (c[1] - d[1]) - (a[1] - c[1]) * (c[0] - d[0])
    uq = (a[0] - c[0]) * (a[1] - b[1]) - (a[1] - c[1]) * (a[0] - b[0])
    t = (tq) / (q)
    u = (uq) / (q)

    # check if line actually intersect
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (int(a[0] + t * (b[0] - a[0])), int(a[1] + t * (b[1] - a[1])))
    return None


@dataclass(unsafe_hash=True, eq=True)
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def time_range(self, mn: int, mx: int) -> tuple[int, int]:
        """time within test box"""
        t0x = (mn - self.px) / self.vx
        t1x = (mx - self.px) / self.vx
        t0y = (mn - self.py) / self.vy
        t1y = (mx - self.py) / self.vy
        t0 = max(min(t0x, t1x), min(t0y, t1y), 0)
        t1 = min(max(t0x, t1x), max(t0y, t1y))
        # print(f"{mn} {mx} Times {t0}, {t1}")
        return int(t0), int(t1)

    def path(self, mn: int, mx: int) -> tuple[tuple[int, int], tuple[int, int]]:
        t0, t1 = self.time_range(mn, mx)
        # print(f"{t0=}, {t1=}")
        x0 = self.px + t0 * (self.vx)
        y0 = self.py + t0 * (self.vy)
        x1 = self.px + t1 * (self.vx)
        y1 = self.py + t1 * (self.vy)
        return (x0, y0), (x1, y1)

    def intersects(self, other: "Hailstone", mn: int, mx: int) -> bool:
        p0, p1 = self.path(mn, mx)
        p2, p3 = other.path(mn, mx)

        intersection = line_intersection(p0, p1, p2, p3)
        # Rouding errors mean we actually pick up some intersections just outside the box
        if intersection and mn < intersection[0] < mx and mn < intersection[1] < mx:
            return intersection
        return None

    def get_mc(self, dx: int, dy: int) -> tuple[int, int, int]:
        # y = (mx + c) / q
        m = self.vy - dy
        q = self.vx - dx
        c = self.py * q - self.px * m
        return m, c, q

    def intersection(
        self, other: "Hailstone", dx: int = 0, dy: int = 0
    ) -> tuple[int, int]:
        m1, c1, q1 = self.get_mc(dx, dy)
        m2, c2, q2 = other.get_mc(dx, dy)
        num = q1 * c2 - c1 * q2
        denom = q2 * m1 - m2 * q1
        if denom != 0 and num % denom == 0:
            x = num // denom
            ynum = m1 * x + c1
            if q1 != 0 and ynum % q1 == 0:
                return x, ynum // q1
        return None


def parse(input: list[str]) -> list[Hailstone]:
    stones: list[Hailstone] = []
    for line in input:
        left, _, right = line.partition(" @ ")
        px, py, pz = [int(n.strip()) for n in left.split(",")]
        vx, vy, vz = [int(n.strip()) for n in right.split(",")]
        stones.append(Hailstone(px, py, pz, vx, vy, vz))
    return stones


def part1(input: list[str], mn: int, mx: int) -> int:
    stones = parse(input)
    return sum(
        1 if s1.intersects(s2, mn, mx) else 0 for s1, s2 in combinations(stones, 2)
    )


res = part1(TEST_DATA, TEST_MIN, TEST_MAX)
assert res == EXPECTED

BOX_MIN = 200000000000000
BOX_MAX = 400000000000000
print(f"{part1(input, BOX_MIN, BOX_MAX)=}")  # 16050

# Part 2
# Brute forces dx,dy in a spiral out from the origin
#
# Find intersection of points (completely ignoring any boxes or the fact they are segments)
# but adjusting velocity by dx,dy (so in a moving frame of reference)
# If all lines intersect at the same point that means in the moving reference frame a stationary
# stone would hit all hailstones, so starting from the same point in a fixed frame
# a stone moving at dx,dy would hit all hailstones.
#
# Only integer coordinates are useful for the intersections so we ignore any non-integer results.
#
# Finally swap x<->z on all hailstones and repeat the search (but only for the same y) to get
# the z, vz values.


def xy(mx: int) -> Sequence[tuple[int, int]]:
    """Yield x,y coordinates in a spiral out from the origin"""
    yield 0, 0
    for x in range(1, mx):
        for y in range(-x, x + 1):
            yield x, y
        for nx in range(x - 1, -x - 1, -1):
            yield nx, x
        for y in range(x - 1, -x - 1, -1):
            yield -x, y
        for nx in range(-x + 1, x):
            yield nx, -x


def get_xy(stones: list[Hailstone], seq: object) -> tuple[int, int, int, int]:
    s1 = stones[0]
    s2 = stones[1]
    others = stones[2:]
    for x, y in seq:
        point = s1.intersection(s2, x, y)
        if point is not None and all(s1.intersection(s, x, y) == point for s in others):
            # print(f"Point {point} at v = ({x}, {y})")
            return point[0], point[1], x, y


def part2(input: list[str]) -> int:
    stones = parse(input)
    s1, s2, s3 = stones[0:3]

    x, y, dx, dy = get_xy(stones, xy(1000))

    # Switch x/z to find z!
    z, y1, dz, dy1 = get_xy(
        [Hailstone(s.pz, s.py, s.px, s.vz, s.vy, s.vx) for s in stones],
        [(n, dy) for n in range(1000)],
    )
    print(f"Found {Hailstone(x, y, z, dx, dy, dz)}")
    return x + y + z


res = part2(TEST_DATA)
assert res == 47

print(f"{part2(input)=}")
# 669042940632377

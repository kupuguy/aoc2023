from pathlib import Path
from typing import Sequence
from functools import cache
from pprint import pprint
from collections import deque
import re
from typing import Callable
from operator import lt, gt
from dataclasses import dataclass
from math import lcm

input = Path("input/day21.txt").read_text().strip().splitlines()

TEST_DATA = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()

EXPECTED = 16


def parse(input: list[str]) -> tuple[tuple[int, int], set(tuple[int, int])]:
    gardens: set[tuple[int, int]] = set()
    start = (0, 0)
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == ".":
                gardens.add((x, y))
            elif c == "S":
                start = (x, y)
                gardens.add((x, y))
    return start, gardens


def neighbours(
    point: tuple[int, int], gardens: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    px, py = point
    return [
        (x, y)
        for (x, y) in [(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)]
        if (x, y) in gardens
    ]


def next_locations(
    points: set[tuple[int, int]], gardens: set[tuple[int, int]], width: int, height: int
):
    return {p for point in points for p in neighbours(point, gardens)}


def part1(input: list[str], nsteps: int = 64) -> int:
    start, gardens = parse(input)
    width, height = len(input[0]), len(input)
    reachable = {start}
    for step in range(nsteps):
        reachable = next_locations(reachable, gardens, width, height)
    return len(reachable)


res = part1(TEST_DATA, 6)
assert res == EXPECTED
print(f"{part1(input)=}")


def neighbours(
    point: tuple[int, int], gardens: set[tuple[int, int]], width, height
) -> list[tuple[int, int]]:
    """Now handles infinite grid!"""
    px, py = point
    return [
        (x, y)
        for (x, y) in [(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)]
        if (x % width, y % height) in gardens
    ]


def next_locations(
    points: set[tuple[int, int]], gardens: set[tuple[int, int]], width: int, height: int
):
    return {p for point in points for p in neighbours(point, gardens, width, height)}


"""
Gave up trying to count the grid and based this solution on someone else's :-( 

    After some starting noise the pattern cycles every [gridsize] iterations.
    So divide the target steps by the grid size and use the remainder as an offset
    then find the quadratic that fits the first three iterations.

See https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keb6a53/


"""


def simplifiedLagrange(y0: int, y1: int, y2: int) -> tuple[int, int, int]:
    """
    Lagrange's Interpolation formula for ax^2 + bx + c with x=[0,1,2] and y=[y0,y1,y2] we have
       f(x) = (x^2-3x+2) * y0/2 - (x^2-2x)*y1 + (x^2-x) * y2/2
    so the coefficients are:
     a = y0/2 - y1 + y2/2
     b = -3*y0/2 + 2*y1 - y2/2
     c = y0
    """
    return y0 / 2 - y1 + y2 / 2, -3 * (y0 / 2) + 2 * y1 - y2 / 2, y0


def part2(input: list[str], nsteps: int = 26501365) -> int:
    grid_size = len(input)
    remainder = nsteps % grid_size
    target = nsteps // grid_size
    values = [
        part1(input, remainder),
        part1(input, remainder + grid_size),
        part1(input, remainder + 2 * grid_size),
    ]
    print(values)
    poly = simplifiedLagrange(*values)
    print(poly)
    a, b, c = poly
    return int(a * target * target + b * target + c)


res = part2(input)
print(f"{res=}")
# 604592315958630

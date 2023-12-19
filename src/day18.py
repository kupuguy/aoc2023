from pathlib import Path
from typing import Sequence
from functools import cache
from pprint import pprint
from collections import deque
import re

input = Path("input/day18.txt").read_text().strip().splitlines()

TEST_DATA = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()

EXPECTED = 62


def parse(input: list[str]) -> list[tuple[str, int]]:
    res: list[tuple[str, int, int]] = []
    for line in input:
        dir, count, colour = line.split()
        res.append((dir, int(count)))
    return res


def dig(data: list[tuple[str, int]]) -> list[list[str]]:
    x, y, top, bottom, left, right = 0, 0, 0, 0, 0, 0
    for d, n in data:
        if d == "U":
            y -= n
            top = min(top, y)
        elif d == "D":
            y += n
            bottom = max(bottom, y)
        elif d == "L":
            x -= n
            left = min(left, x)
        else:
            x += n
            right = max(right, x)
    width = right - left + 3
    height = bottom - top + 3
    startx = -left + 1
    starty = -top + 1
    print(f"{startx=}, {starty=}, {width=}, {height=}")

    grid = [["."] * width for n in range(height)]
    x, y = startx, starty
    for d, n in data:
        if d == "U":
            for i in range(n):
                y -= 1
                grid[y][x] = "#"
        elif d == "D":
            for i in range(n):
                y += 1
                grid[y][x] = "#"
        elif d == "L":
            for i in range(n):
                x -= 1
                grid[y][x] = "#"
        else:
            for i in range(n):
                x += 1
                grid[y][x] = "#"

    # print('\n'.join(''.join(row) for row in grid))
    return grid


def fill_outside(grid: list[list[str]]) -> int:
    width, height = len(grid[0]), len(grid)
    points = deque([(0, 0)])
    count = 0
    while points:
        x, y = points.popleft()
        if grid[y][x] != ".":
            continue
        grid[y][x] = "!"
        count += 1
        for x1, y1 in [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]:
            if 0 <= x1 < width and 0 <= y1 < height and grid[y1][x1] == ".":
                points.append((x1, y1))

    # print('\n'.join(''.join(row) for row in grid))
    print(width, height, width * height, count)
    return width * height - count


def part1(input: list[str]):
    data = parse(input)
    grid = dig(data)
    return fill_outside(grid)


res = part1(TEST_DATA)
print(f"Test={res}")
assert res == EXPECTED
print(part1(input))  # 46334


def parse2(input: list[str]) -> list[tuple[int, int]]:
    res: list[tuple[str, int, int]] = []
    directions = {0: "R", 1: "D", 2: "L", 3: "U"}
    for line in input:
        dir, count, colour = line.split()
        res.append((directions[int(colour[-2])], int(colour[2:-2], 16)))
    return res


def dig2(data: list[tuple[str, int]]) -> int:
    x, y = 0, 0
    inside = 1
    for d, n in data:
        if d == "U":
            inside -= n * (x - 1)
            y -= n
        elif d == "D":
            inside += n * x
            y += n
        elif d == "L":
            x -= n
        else:
            inside += n
            x += n

    return inside


def part2a(input: list[str]):
    data = parse(input)
    volume = dig2(data)
    return volume


EXPECTED2 = 952408144115

res = part2a(TEST_DATA)
print(f"Test={res}")
assert res == EXPECTED
assert part2a(input) == 46334


def part2(input: list[str]):
    data = parse2(input)
    volume = dig2(data)
    return volume


res = part2(TEST_DATA)
print(f"Test={res}")
assert res == EXPECTED2
print(part2(input))
# 102000662718092

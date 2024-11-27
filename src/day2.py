import pathlib

input = pathlib.Path("../input/day2.txt").read_text().splitlines()

TEST_DATA = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED = 8


def parse(line: str) -> (int, list[tuple[int, int, int]]):
    g, rest = line.strip().split(": ")
    id = int(g.split()[-1])
    parts: list[tuple[int, int, int]] = []
    for draw in rest.split(";"):
        got = {"red": 0, "green": 0, "blue": 0}
        for cube in draw.strip().split(", "):
            n, colour = cube.split()
            got[colour] = int(n)
        parts.append((got["red"], got["green"], got["blue"]))
    return id, parts


def part1(input: list[str], maxr: int = 12, maxg: int = 13, maxb: int = 14) -> int:
    total = 0
    for line in input:
        if not line:
            continue
        id, parts = parse(line)
        # print(id, parts)
        if all(r <= maxr and g <= maxg and b <= maxb for r, g, b in parts):
            total += id
    return total


test_value = part1(TEST_DATA.splitlines())
assert test_value == EXPECTED

print(part1(input))

EXPECTED2 = 2286


def part2(input: list[str], maxr: int = 12, maxg: int = 13, maxb: int = 14) -> int:
    total = 0
    for line in input:
        if not line:
            continue
        id, parts = parse(line)
        # print(id, parts)
        r = max(r for r, g, b in parts)
        g = max(g for r, g, b in parts)
        b = max(b for r, g, b in parts)
        total += r * g * b
    return total


test_value = part2(TEST_DATA.splitlines())
assert test_value == EXPECTED2

print(part2(input))

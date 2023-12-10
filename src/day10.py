from pathlib import Path
from typing import Sequence

input = Path("input/day10.txt").read_text().splitlines()


TEST_DATA = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()

"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal;"""


def neighbours(x: int, y: int, input: list[str]) -> Sequence[tuple[int, int]]:
    N = x, y - 1
    S = x, y + 1
    E = x + 1, y
    W = x - 1, y
    match input[y][x]:
        case "|":
            neighbours = N, S
        case "-":
            neighbours = E, W
        case "L":
            neighbours = N, E
        case "J":
            neighbours = N, W
        case "7":
            neighbours = S, W
        case "F":
            neighbours = S, E
        case "S":
            neighbours = N, S, E, W
        case _:
            neighbours = ()
    return [
        d for d in neighbours if 0 <= d[1] < len(input) and 0 <= d[0] <= len(input[0])
    ]


def part1(input: list[str]) -> int:
    start = [(line.index("S"), row) for row, line in enumerate(input) if "S" in line][0]
    print(f"{start=}")
    distances = {start: 0}
    queue = [start]
    while queue:
        current = queue.pop(0)
        curdist = distances[current]
        nxt = [
            n
            for n in neighbours(current[0], current[1], input)
            if current in neighbours(n[0], n[1], input)
        ]
        # print(current, nxt, curdist, [distances[n] for n in nxt if n in distances])
        if len(nxt) == 2 and all(n in distances for n in nxt):
            # print(nxt)
            # print(distances)
            # print(f"{curdist=}")
            return curdist + 1
        for n in nxt:
            if n not in distances:
                distances[n] = curdist + 1
                queue.append(n)
    assert False


EXPECTED = 8

assert part1(TEST_DATA) == EXPECTED
print(part1(input))


def loop_path(input: list[str]) -> set[tuple[int, int]]:
    start = [(line.index("S"), row) for row, line in enumerate(input) if "S" in line][0]
    print(f"{start=}")
    distances = {start: 0}
    paths = {start: {start}}
    queue = [start]
    while queue:
        current = queue.pop(0)
        curdist = distances[current]
        nxt = [
            n
            for n in neighbours(current[0], current[1], input)
            if current in neighbours(n[0], n[1], input)
        ]
        if len(nxt) == 2 and all(n in distances for n in nxt):
            return paths[nxt[0]] | paths[nxt[1]] | {current}

        for n in nxt:
            if n not in distances:
                distances[n] = curdist + 1
                paths[n] = paths[current] | {n}
                queue.append(n)
    assert False


def fix_start(input: list[str], path: set[tuple[int, int]]) -> list[str]:
    start_x, start_y = [
        (line.index("S"), row) for row, line in enumerate(input) if "S" in line
    ][0]
    if (start_x + 1, start_y) in path and input[start_y][start_x + 1] in "7-J":
        if (start_x - 1, start_y) in path and input[start_y][start_x - 1] in "L-F":
            start = "-"
        elif (start_x, start_y + 1) in path and input[start_y + 1][start_x] in "L|J":
            start = "F"
        else:
            assert (start_x, start_y - 1) in path and input[start_y - 1][
                start_x
            ] in "F|7"
            start = "L"
    elif (start_x - 1, start_y) in path and input[start_y][start_x - 1] in "L-F":
        if (start_x, start_y - 1) in path and input[start_y - 1][start_x] in "F|7":
            start = "J"
        else:
            assert (start_x, start_y + 1) in path and input[start_y + 1][
                start_x
            ] in "L|J"
            start = "7"
    else:
        assert (
            (start_x, start_y - 1) in path
            and input[start_y - 1][start_x] in "F|7"
            and (start_x, start_y + 1) in path
            and input[start_y + 1][start_x] in "L|J"
        )
        start = "|"
    print(f"{start=}")
    return [line.replace("S", start) for line in input]


def part2(input: list[str]) -> int:
    area = 0
    path = loop_path(input)
    input = fix_start(input, path)
    for y in range(0, len(input)):
        row = "".join(c if (x, y) in path else "." for x, c in enumerate(input[y]))
        row = (
            row.replace("-", "")
            .replace("FJ", "|")
            .replace("L7", "|")
            .replace("F7", "")
            .replace("LJ", "")
        )
        IN_LOOP = False
        for c in row:
            if c == "|":
                IN_LOOP = not IN_LOOP
            elif IN_LOOP and c == ".":
                area += 1
    return area


TEST_DATA = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()

print(sorted([p for p in loop_path(TEST_DATA) if p[1] == 3]))
print(f"{part2(TEST_DATA)=}")
assert part2(TEST_DATA) == 10
print(part2(input))  # 413

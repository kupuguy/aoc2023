from pathlib import Path
from typing import Sequence
from functools import cache

input = Path("input/day16.txt").read_text().strip().splitlines()

TEST_DATA = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....""".splitlines()

EXPECTED = 46


def calc_beams(
    input: list[str], startx: int, starty: int, dir: str = ">"
) -> list[list[set[str]]]:
    beams: list[tuple[int, int, str]] = [(startx, starty, dir)]
    active: list[list[set[str]]] = [
        [set() for x in range(len(input[0]))] for y in range(len(input))
    ]
    assert len(active) == len(input) and len(active[0]) == len(input[0])
    while beams:
        x, y, dir = beams.pop()
        deltax, deltay = (
            (1, 0)
            if dir == ">"
            else (-1, 0)
            if dir == "<"
            else (0, -1)
            if dir == "^"
            else (0, 1)
        )
        # print(x, y, dir, deltax, deltay, active[y][x], input[y][x])
        while (
            0 <= x < len(input[0]) and 0 <= y < len(input) and dir not in active[y][x]
        ):
            # print("->", x, y, active[y][x], input[y][x])
            active[y][x].add(dir)
            match input[y][x]:
                case ".":
                    x += deltax
                    y += deltay
                case "|":
                    if dir in "><":
                        beams.append((x, y - 1, "^"))
                        beams.append((x, y + 1, "v"))
                        break
                    x += deltax
                    y += deltay
                    if x < 0 or x > len(input[0]) or y < 0 or y > len(input):
                        break

                case "-":
                    if dir in "^v":
                        beams.append((x - 1, y, "<"))
                        beams.append((x + 1, y, ">"))
                        break
                    x += deltax
                    y += deltay
                    if x < 0 or x > len(input[0]) or y < 0 or y > len(input):
                        break
                case "\\":
                    deltax, deltay, dir = (
                        (0, 1, "v")
                        if dir == ">"
                        else (0, -1, "^")
                        if dir == "<"
                        else (-1, 0, "<")
                        if dir == "^"
                        else (1, 0, ">")
                    )
                    beams.append((x + deltax, y + deltay, dir))
                    # print("\\ -> ", x, y, beams[-1])
                    break
                case "/":
                    deltax, deltay, dir2 = (
                        (0, -1, "^")
                        if dir == ">"
                        else (0, 1, "v")
                        if dir == "<"
                        else (1, 0, ">")
                        if dir == "^"
                        else (-1, 0, "<")
                    )
                    beams.append((x + deltax, y + deltay, dir2))
                    # print(f"/ {dir} -> ", x, y, beams[-1])
                    break
                case _:
                    raise RuntimeError("gone wrong")
    return active


def show(input, active):
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == ".":
                if len(active[y][x]) == 1:
                    print(list(active[y][x])[0], end="", sep="")
                elif len(active[y][x]) > 1:
                    print("2", end="", sep="")
                else:
                    print(c, end="", sep="")
            else:
                print(c, end="", sep="")
        print()
    print()


def part1(input: list[str], startx: int = 0, starty: int = 0, dir: str = ">") -> int:
    active = calc_beams(input, startx, starty, dir)
    # show(input, active)
    return sum(1 for row in active for state in row if state)


assert part1(TEST_DATA) == EXPECTED
print("Part 1 ->", part1(input))


def part2(input: list[str]) -> int:
    return max(
        max(part1(input, 0, y, ">") for y in range(len(input))),
        max(part1(input, len(input[0]) - 1, y, "<") for y in range(len(input))),
        max(part1(input, x, len(input) - 1, "^") for x in range(len(input[0]))),
        max(part1(input, x, 0, "v") for x in range(len(input[0]))),
    )


assert part2(TEST_DATA) == 51
print("Part 2 ->", part2(input))

from itertools import pairwise
from pathlib import Path

input = Path("input/day9.txt").read_text().splitlines()


TEST_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()

EXPECTED = 114


def compute_next(values: list[int]) -> int:
    # print(values)
    if all(v == 0 for v in values):
        # print("->", 0)
        return 0
    diffs = [b - a for a, b in pairwise(values)]
    nxt = compute_next(diffs) + values[-1]
    # print("->", nxt)
    return nxt


def next_in_seq(line: str) -> int:
    values = [int(w) for w in line.strip().split()]
    return compute_next(values)


def part1(input: list[str]) -> int:
    return sum(next_in_seq(line) for line in input)


assert part1(TEST_DATA) == EXPECTED
print(part1(input))


def compute_prev(values: list[int]) -> int:
    # print(values)
    if all(v == 0 for v in values):
        # print("->", 0)
        return 0
    diffs = [b - a for a, b in pairwise(values)]
    nxt = values[0] - compute_prev(diffs)
    # print("->", nxt)
    return nxt


def prev_in_seq(line: str) -> int:
    values = [int(w) for w in line.strip().split()]
    return compute_prev(values)


def part2(input: list[str]) -> int:
    return sum(prev_in_seq(line) for line in input)


assert part2(TEST_DATA) == 2
print(part2(input))

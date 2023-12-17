from pathlib import Path
from typing import Sequence
from functools import cache
from collections import deque
from pprint import pprint

input = Path("input/day17.txt").read_text().strip().splitlines()

TEST_DATA = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()

EXPECTED = 102

LEFT = {1: -1j, 1j: 1, -1j: -1, -1: 1j}
RIGHT = {1: 1j, 1j: -1, -1j: 1, -1: -1j}
LIFE = 3


def shortest_path(
    grid: dict[complex, int], start: complex, end: complex, size: complex
) -> int:
    def maybe_move(pos: complex, life: int, dir: complex, cost: int):
        for n in range(life, 0, -1):
            if 0 <= pos.real < size.real and 0 <= pos.imag < size.imag:
                cost += grid[pos]
                if pos not in costs[dir] or costs[dir][pos] > cost:
                    costs[dir][pos] = cost
                    moves.append((pos, n, dir, cost))
            pos += dir

    costs: dict[complex, dict[complex, int]] = {
        1
        + 0j: {
            start: 0,
        },
        1j: {
            start: 0,
        },
        -1
        + 0j: {
            start: 0,
        },
        -1j: {
            start: 0,
        },
    }
    moves = deque([])
    maybe_move(start + 1, LIFE, 1, 0)
    maybe_move(start + 1j, LIFE, 1j, 0)

    while moves:
        pos, life, curdir, current_cost = moves.popleft()
        maybe_move(pos + LEFT[curdir], LIFE, LEFT[curdir], current_cost)
        maybe_move(pos + RIGHT[curdir], LIFE, RIGHT[curdir], current_cost)
    #     if len(moves > 12):
    #         print(moves)
    #         print(costs)
    #         exit()
    # show(costs, size)
    return min(c[end] for c in costs.values() if end in c)


def show(grid: dict[complex, dict[complex, int]], size: complex) -> None:
    clean = grid[1].copy()
    for dir in (-1 + 0j, 1j, -1j):
        for k, v in grid[dir].items():
            if k in clean:
                clean[k] = min(v, clean[k])
            else:
                clean[k] = v

    for y in range(int(size.imag)):
        for x in range(int(size.real)):
            print(f"{clean[x+y*1j]:4}", end=" ")
        print()


def part1(input: list[str]) -> int:
    grid = {
        x + (y * 1j): int(c) for y, line in enumerate(input) for x, c in enumerate(line)
    }
    size = complex(len(input[0]), len(input))
    return shortest_path(grid, 0 + 0j, size - (1 + 1j), size)


res = part1(TEST_DATA)
assert res == EXPECTED

# print("Part 1 ->", part1(input))
# 694


def ultra_path(
    grid: dict[complex, int], start: complex, end: complex, size: complex
) -> int:
    def maybe_move(pos: complex, dir: complex, cost: int):
        for n in range(1, 4):
            if 0 <= pos.real < size.real and 0 <= pos.imag < size.imag:
                cost += grid[pos]
                # if pos not in costs[dir] or costs[dir][pos] > cost:
                #     costs[dir][pos] = cost
            pos += dir

        for n in range(4, 11):
            if 0 <= pos.real < size.real and 0 <= pos.imag < size.imag:
                cost += grid[pos]
                if pos not in costs[dir] or costs[dir][pos] > cost:
                    costs[dir][pos] = cost
                    moves.append((pos, dir, cost))
            pos += dir

    costs: dict[complex, dict[complex, int]] = {
        1
        + 0j: {
            start: 0,
        },
        1j: {
            start: 0,
        },
        -1
        + 0j: {
            start: 0,
        },
        -1j: {
            start: 0,
        },
    }
    moves = deque([])
    maybe_move(start + 1, 1, 0)
    maybe_move(start + 1j, 1j, 0)

    while moves:
        pos, curdir, current_cost = moves.popleft()
        maybe_move(pos + LEFT[curdir], LEFT[curdir], current_cost)
        maybe_move(pos + RIGHT[curdir], RIGHT[curdir], current_cost)
        # if len(moves) > 12:
        #     pprint(moves)
        #     pprint(costs)
        #     exit()
    # show(costs, size)
    return min(c[end] for c in costs.values() if end in c)


def part2(input: list[str]) -> int:
    grid = {
        x + (y * 1j): int(c) for y, line in enumerate(input) for x, c in enumerate(line)
    }
    size = complex(len(input[0]), len(input))
    return ultra_path(grid, 0 + 0j, size - (1 + 1j), size)


# res = part2(TEST_DATA)
# print("Test", res)
# assert res == 94

TD2 = """111111111111
999999999991
999999999991
999999999991
999999999991""".splitlines()
res = part2(TD2)
print("Test2", res)
assert res == 71

print("Part 2 ->", part2(input))
# < 849

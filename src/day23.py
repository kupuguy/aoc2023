from pathlib import Path
from typing import Sequence
from functools import cache
from pprint import pprint
from collections import deque
import re
from typing import Callable
from operator import lt, gt
from dataclasses import dataclass, field
from string import ascii_uppercase

input = Path("input/day23.txt").read_text().strip().splitlines()

TEST_DATA = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()

EXPECTED = 94


def neighbours(x: int, y: int, grid: list[str]) -> list[tuple[int, int]]:
    return [
        (x1, y1)
        for (x1, y1) in [(x + 1, y), (x, y + 1)]
        if 0 <= x1 < len(grid[0]) and 0 <= y1 < len(grid) and grid[y1][x1] in ".>v"
    ] + [
        (x1, y1)
        for (x1, y1) in [(x - 1, y), (x, y - 1)]
        if 0 <= x1 < len(grid[0]) and 0 <= y1 < len(grid) and grid[y1][x1] in "."
    ]


def paths(
    grid: list[str], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    visited: set(tuple[int, int]) = {start}
    stack = [[start]]
    print(f"{start=}, {end=}")
    while stack:
        current = stack[-1][-1]
        visited.add(current)
        if current == end:
            print(len(visited) - 1)
            yield visited - {start}
        else:
            nxt = [
                n for n in neighbours(current[0], current[1], grid) if n not in visited
            ]
            if nxt:
                stack.append(nxt)
                continue
        # backtrack
        while stack:
            p = stack[-1].pop(-1)
            visited.remove(p)
            if stack[-1]:
                break
            del stack[-1]


def show(grid: list[str], visited: set[tuple[int, int]]) -> None:
    for y, line in enumerate(grid):
        row = "".join("O" if (x, y) in visited else c for x, c in enumerate(line))
        print(row)


def part1(input: list[str]) -> int:
    longest = max(
        paths(input, (1, 0), (len(input[0]) - 2, len(input) - 1)), key=lambda p: len(p)
    )
    show(input, longest)
    return len(longest)


# res = part1(TEST_DATA)
# print("Test", res)
# assert res == EXPECTED

# print(f"{part1(input)=}")


def neighbours2(x: int, y: int, grid: list[str]) -> list[tuple[int, int]]:
    return [
        (x1, y1)
        for (x1, y1) in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        if 0 <= x1 < len(grid[0]) and 0 <= y1 < len(grid) and grid[y1][x1] in ".>v"
    ]


@dataclass(unsafe_hash=True, eq=True)
class Node:
    x: int
    y: int

    neighbour_distances: dict[tuple[int, int], int] = field(
        default_factory=dict, init=False, hash=False, repr=False
    )


def parse_nodes(grid: list[str]):
    nodes: dict[tuple[int, int], Node] = {}
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "#":
                continue
            n = Node(x, y)
            for nxt in neighbours2(x, y, grid):
                n.neighbour_distances[nxt] = 1
            nodes[x, y] = n

    print(f"Full grid has {len(nodes)} nodes")

    for xy in list(nodes):
        n = nodes[xy]
        if len(n.neighbour_distances) == 2:
            a, b = list(n.neighbour_distances)
            distance = n.neighbour_distances[a] + n.neighbour_distances[b]
            prev = nodes[a]
            nxt = nodes[b]
            del nodes[xy]
            nodes[a].neighbour_distances[b] = distance
            nodes[b].neighbour_distances[a] = distance
            del nodes[a].neighbour_distances[xy]
            del nodes[b].neighbour_distances[xy]
    print(f"Found {len(nodes)} nodes")
    return nodes


def node_paths(
    nodes: dict[tuple[int, int], Node], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    visited: dict[tuple[int, int], int] = {start: 0}
    stack: list[list[tuple[tuple[int, int], int]]] = [[(start, 0)]]
    print(f"{start=}, {end=}")
    while stack:
        current_xy, distance = stack[-1][-1]
        current = nodes[current_xy]
        visited[current_xy] = distance
        nxt = {
            nxt_xy: d + distance
            for nxt_xy, d in current.neighbour_distances.items()
            if nxt_xy not in visited
        }

        if end in nxt:
            # print(nxt[end])
            yield nxt[end]
            del nxt[end]

        if nxt:
            stack.append(list(nxt.items()))
            continue

        # backtrack
        while stack:
            xy, d = stack[-1].pop(-1)
            del visited[xy]
            if stack[-1]:
                break
            del stack[-1]


def part2(input: list[str]) -> int:
    nodes = parse_nodes(input)
    longest = max(
        node_paths(nodes, (1, 0), (len(input[0]) - 2, len(input) - 1)),
    )
    return longest


assert part2(TEST_DATA) == 154
print(f"{part2(input)=}")

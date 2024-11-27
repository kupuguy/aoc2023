from itertools import cycle
from math import gcd
from pathlib import Path
from typing import Sequence

input = Path("input/day8.txt").read_text().splitlines()


TEST_DATA = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".splitlines()

EXPECTED = 6


def parse(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    network: dict[str, tuple[str, str]] = {}
    moves = lines[0]
    for line in lines[2:]:
        name, left, right = line[:3], line[7:10], line[12:15]
        network[name] = (left, right)
    return moves, network


def part1(input: list[str]) -> int:
    moves, network = parse(input)
    node = "AAA"
    for count, move in enumerate(cycle(moves), start=1):
        node = network[node][0 if move == "L" else 1]
        if node == "ZZZ":
            break
    return count


assert part1(TEST_DATA) == EXPECTED
print(part1(input))

TEST_DATA2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".splitlines()


def all_distances(
    node: str, moves: str, network: dict[str, tuple[str, str]]
) -> Sequence[int]:
    distances: dict[str, set[int]] = {}
    for count, move in enumerate(cycle(moves), start=1):
        node = network[node][0 if move == "L" else 1]
        if node.endswith("Z"):
            if node in distances:
                if count % len(moves) in distances[node]:
                    return
                else:
                    distances[node].add(count % len(moves))
            else:
                distances[node] = {count % len(moves)}
            yield count


def lcm(a: int, b: int):
    return int(abs(a * b) / gcd(a, b))


def part2(input: list[str]) -> int:
    moves, network = parse(input)
    start_nodes = {n for n in network if n.endswith("A")}
    distances: dict[str, list[int]] = {}
    possible = {1}
    for n in start_nodes:
        distances = list(all_distances(n, moves, network))
        possible = {lcm(p, d) for p in possible for d in distances}
    return min(possible)


assert part2(TEST_DATA2) == 6
print(part2(input))
# 18625484023687

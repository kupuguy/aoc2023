from pathlib import Path
from typing import Sequence
from functools import cache

input = Path("input/day13.txt").read_text().splitlines()

TEST_DATA = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()

EXPECTED = 405


def blocks(input: list[str]) -> Sequence[list[str]]:
    block: list[str] = []
    for line in input:
        if line:
            block.append(line)
        else:
            if block:
                yield block
            block = []
    if block:
        yield block


def transpose(lines: list[str]) -> list[str]:
    return ["".join(s) for s in zip(*lines)]


def reflections(block: list[str]) -> Sequence[int]:
    for index in range(1, len(block)):
        nrange = min(index, len(block) - index)
        # print(len(block), index, index - (nrange-1) - 1, index + nrange-1)
        if all(block[index - n - 1] == block[index + n] for n in range(nrange)):
            yield index


def part1(input: list[str]) -> int:
    total = 0
    for block in blocks(input):
        # print(*block, sep="\n")
        total += sum(reflections(block)) * 100

        transposed = transpose(block)
        # print(*transpose(block), sep="\n")
        total += sum(reflections(transposed))

    return total


res = part1(TEST_DATA)
assert res == EXPECTED

print(part1(input))
# > 20700


def diff_by_one(line1: str, line2: str) -> bool:
    return sum(1 if a != b else 0 for a, b in zip(line1, line2)) == 1


def smudged(block: list[str]) -> int:
    for index in range(1, len(block)):
        nrange = min(index, len(block) - index)
        # print(len(block), index, index - (nrange-1) - 1, index + nrange-1)
        seen_diff = False
        match = True
        for n in range(nrange):
            if block[index - n - 1] != block[index + n]:
                if not seen_diff and diff_by_one(
                    block[index - n - 1], block[index + n]
                ):
                    seen_diff = True
                    continue
                match = False
                break
        if match and seen_diff:
            return index
    return 0


def part2(input: list[str]) -> int:
    total = 0
    for block in blocks(input):
        total += smudged(block) * 100

        transposed = transpose(block)
        # print(*transpose(block), sep="\n")
        total += smudged(transposed)

    return total


assert part2(TEST_DATA) == 400
print(part2(input))

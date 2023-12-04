from pathlib import Path
import re

input = Path("input/day4.txt").read_text().splitlines()


TEST_DATA = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()

EXPECTED = 13


def parse(line: str) -> tuple[set, set]:
    card, rest = line.split(":")
    have, want = rest.split("|")
    return set(int(n) for n in have.strip().split()), set(
        int(n) for n in want.strip().split()
    )


def part1(input: list[str]) -> int:
    total = 0
    for card in input:
        have, want = parse(card)
        matches = len(have & want)
        if matches:
            total += 1 << (matches - 1)
    return total


result = part1(TEST_DATA)
assert result == EXPECTED

print(part1(input))

EXPECTED2 = 30


def part2(input: list[str]):
    cards = [1] * len(input)
    for index, card in enumerate(input):
        have, want = parse(card)
        wins = len(have & want)
        for i in range(1, wins + 1):
            cards[index + i] += cards[index]
        # print(cards)
    return sum(cards)


assert part2(TEST_DATA) == EXPECTED2
print(part2(input))

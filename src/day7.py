from pathlib import Path
from enum import IntEnum
from collections import Counter

input = Path("input/day7.txt").read_text().splitlines()


TEST_DATA = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()

EXPECTED = 6440


class HandType(IntEnum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6


# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
STRENGTHS = "23456789TJQKA"


def parse(lines: list[str]) -> list[tuple[str, int]]:
    hands: list[tuple[str, int]] = []
    for line in lines:
        h, b = line.split()
        hands.append((h, int(b)))
    return hands


def hand_key(hand: tuple[str, int]) -> tuple[int, str]:
    raw_cards, bid = hand
    cards = tuple(STRENGTHS.index(c) for c in raw_cards)
    ordered = Counter(raw_cards).most_common()
    if ordered[0][1] == 5:
        return HandType.FIVE_KIND, cards
    if ordered[0][1] == 4:
        return HandType.FOUR_KIND, cards
    if ordered[0][1] == 3:
        if ordered[1][1] == 2:
            return HandType.FULL_HOUSE, cards
        return HandType.THREE_KIND, cards
    if ordered[0][1] == 2:
        if ordered[1][1] == 2:
            return HandType.TWO_PAIR, cards
        return HandType.ONE_PAIR, cards
    return HandType.HIGH_CARD, cards


def part1(input: list[str]) -> int:
    hands = parse(input)
    hands.sort(key=hand_key)
    total = 0
    for rank, hand_bid in enumerate(hands, start=1):
        hand, bid = hand_bid
        total += bid * rank
    return total


assert part1(TEST_DATA) == EXPECTED
print(part1(input))
# 249483956

from typing import Sequence

STRENGTHS = "J23456789TQKA"


def joker_hands(raw_cards: str) -> Sequence[str]:
    other_cards = set(raw_cards) - {"J"}

    if "J" not in raw_cards or other_cards == set():
        yield raw_cards
        return

    for card in STRENGTHS[1:]:
        cards = raw_cards.replace("J", card, 1)
        yield from joker_hands(cards)


def joker_key(hand: tuple[str, int]) -> tuple[int, str]:
    raw_cards, bid = hand
    hand_type, subst_cards = max(
        hand_key((cards, bid)) for cards in joker_hands(raw_cards)
    )
    cards = tuple(STRENGTHS.index(c) for c in raw_cards)
    print(hand_type, raw_cards, subst_cards)
    return (hand_type, cards)


def part2(input: list[str]) -> int:
    hands = parse(input)
    hands.sort(key=joker_key)
    total = 0
    for rank, hand_bid in enumerate(hands, start=1):
        hand, bid = hand_bid
        total += bid * rank
    return total


EXPECTED2 = 5905
assert part2(TEST_DATA) == EXPECTED2
print(part2(input))
# 252137472

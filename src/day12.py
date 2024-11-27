from functools import cache
from pathlib import Path
from typing import Sequence

input = Path("input/day12.txt").read_text().splitlines()


TEST_DATA = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()
EXPECTED = 21


def parse(input: list[str]) -> Sequence[tuple[str, list[int]]]:
    for line in input:
        left, right = line.strip().split()
        yield left, [int(n) for n in right.split(",")]


@cache
def matches(mask: str, values: tuple[int]) -> int:
    # print(mask, values)
    if not values:
        return 0 if "#" in mask else 1

    current = values[0]
    rest = values[1:]
    if current == len(mask) and "." not in mask and not rest:
        return 1

    rightmost = len(mask) - (sum(rest) + (len(rest) - 1)) - current
    total = 0
    # print(f"{rightmost=}, {rest=}")
    for pos in range(0, rightmost):
        left, masked, sep, right = (
            mask[:pos],
            mask[pos : pos + current],
            mask[pos + current : pos + current + 1],
            mask[pos + current + 1 :],
        )
        if "#" in left:
            # no more matches possible
            return total
        if "." not in masked and sep in (".", "?", ""):
            n = matches(right, rest)
            # print(f"{left}[{masked}]{sep}{right} -> {n}")
            total += n
    return total


assert matches("?###????????", (3, 2, 1)) == 10
assert matches("???.###", (1, 1, 3)) == 1
assert matches(".??..??...?##.", (1, 1, 3)) == 4


def part1(input: list[str], unfold: bool = False) -> int:
    total = 0
    for mask, values in parse(input):
        if unfold:
            mask = "?".join([mask] * 5)
            values = values * 5
        n = matches(mask, tuple(values))
        # print(f"{n}: {mask} {values}")
        total += n
    return total


res = part1(TEST_DATA)
assert res == EXPECTED

print(part1(input))

assert part1(TEST_DATA, unfold=True) == 525152
print(part1(input, unfold=True))  # 204640299929836

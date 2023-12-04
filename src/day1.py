import re

DATA = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".split()

EXPECTED = 142


def value(line: str) -> int:
    digits = "".join(d for d in line if d.isdigit())
    if digits:
        # print("Found", digits[0], digits[-1])
        return int(digits[0] + digits[-1])
    return 0


def part1(data: list[str]) -> int:
    return sum(value(line) for line in data)


test1 = part1(DATA)
print(test1)
assert test1 == EXPECTED

from pathlib import Path

input = Path("input/day1.txt").read_text().split("\n")
print(part1(input))

DATA = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""".split()

SUBST = {
    "one": "1e",
    "two": "2o",
    "three": "3e",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7n",
    "eight": "8t",
    "nine": "9e",
}


def value2(line: str) -> int:
    line2 = re.sub(
        "one|two|three|four|five|six|seven|eight|nine",
        lambda m: str(SUBST[m.group(0)]),
        line,
    )
    line2 = re.sub(
        "one|two|three|four|five|six|seven|eight|nine",
        lambda m: str(SUBST[m.group(0)]),
        line2,
    )

    digits = [d for d in line2 if d.isdigit()]
    if digits:
        if line != line2:
            print(line, "=>", line2, "=>", digits[0] + digits[-1])
        return int(digits[0] + digits[-1])
    return 0


def part2(data: list[str]) -> int:
    return sum(value2(line) for line in data)


assert part2(DATA) == 281

print("part2", part2(input))

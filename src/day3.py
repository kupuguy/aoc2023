import pathlib
import re

input = pathlib.Path("input/day3.txt").read_text().splitlines()

TEST_DATA = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".splitlines()

EXPECTED = 4361


def get_parts(prev: str, line: str, next: str):
    parts = []
    prev = re.sub("[0-9]", ".", prev)
    next = re.sub("[0-9]", ".", next)
    # print(prev)
    # print(line)
    # print(next)
    for m in re.finditer("([0-9]+)", line):
        start, end = m.span()
        if start > 0:
            start -= 1
        end += 1
        # print(
        #    start,
        #    end,
        #    prev[start:end],
        #    next[start:end],
        #    (m.start() > 0 and line[m.start() - 1] != "."),
        #    line[m.end() : m.end() + 1] not in (".", ""),
        # )
        if (
            any(c != "." for c in prev[start:end])
            or any(c != "." for c in next[start:end])
            or (m.start() > 0 and line[m.start() - 1] != ".")
            or line[m.end() : m.end() + 1] not in (".", "")
        ):
            parts.append(int(m.group()))
    return parts


def parse(lines: list[str]) -> list[int]:
    parts: list[int] = []
    blank = "." * len(lines[0])
    prev = blank
    for line_no, line in enumerate(lines):
        next = lines[line_no + 1] if line_no < len(lines) - 1 else blank
        parts.extend(get_parts(prev, line, next))
        prev = line
    return parts


def part1(input: list[str]) -> int:
    return sum(parse(input))


test_result = part1(TEST_DATA)
assert test_result == EXPECTED

result = part1(input)
print(result)

EXPECTED2 = 467835


def get_num_at(line: str, index: int) -> tuple[int, int, int]:
    assert line[index].isdigit()
    end = index
    while index > 0 and line[index - 1].isdigit():
        index -= 1
    start = index
    while line[end + 1 : end + 2].isdigit():
        end += 1
    return int(line[start : end + 1]), start, end


def add_value(values: dict, line: str, index: int) -> None:
    if line[index].isdigit():
        v, start, end = get_num_at(line, index)
        values[start, end, line] = v


def grab_adjacent(index: int, prev: str, line: str, next: str) -> list[int]:
    values: dict[tuple[int, int], int] = {}
    if index > 0:
        add_value(values, prev, index - 1)
        add_value(values, line, index - 1)
        add_value(values, next, index - 1)

    add_value(values, prev, index)
    add_value(values, line, index)
    add_value(values, next, index)

    if index < len(line) - 1:
        add_value(values, prev, index + 1)
        add_value(values, line, index + 1)
        add_value(values, next, index + 1)
    return list(values.values())


def parse2(lines: list[str]) -> list[int]:
    gears: list[int] = []
    blank = "." * len(lines[0])
    prev = blank

    for line_no, line in enumerate(lines):
        next = lines[line_no + 1] if line_no < len(lines) - 1 else blank
        print(line)
        for m_star in re.finditer("\*", line):
            # grab all numbers adjacent
            values = grab_adjacent(m_star.start(), prev, line, next)
            print(m_star.start(), values)
            if len(values) >= 2:
                gears.append(values[0] * values[1])
        prev = line
    return gears


def part2(input: list[str]) -> int:
    return sum(parse2(input))


test_result = part2(TEST_DATA)
assert test_result == EXPECTED2
result = part2(input)
assert result > 70317251
print(result)

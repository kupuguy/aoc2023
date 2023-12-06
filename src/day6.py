from pathlib import Path

TEST_DATA = '''Time:      7  15   30
Distance:  9  40  200'''.splitlines()
EXPECTED=288

input = Path('input/day6.txt').read_text().splitlines()

def parse(lines: list[str]) -> list[tuple[int, int]]:
    times = [int(n) for n in lines[0].split(':')[1].strip().split()]
    distances = [int(n) for n in lines[1].split(':')[1].strip().split()]
    return list(zip(times, distances))

def race(time:int, distance:int) -> int:
    return sum(1 for speed in  range(0, time) if (time-speed) * speed > distance)

def part1(input: list[str]) -> int:
    result = 1
    for t,d in parse(input):
        result *= race(t, d)
    return result

assert part1(TEST_DATA) == EXPECTED
print(part1(input))

nospace = '''Time:        42     68     69     85
Distance:   284   1005   1122   1341
'''.replace(' ', '').splitlines()
print(part1(nospace)) # 26187338
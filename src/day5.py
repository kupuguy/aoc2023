from itertools import pairwise
from pathlib import Path

TEST_DATA = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".splitlines()

EXPECTED = 35


def parse(lines: list[str]) -> dict[str, tuple[str, list[tuple[int, int, int]]]]:
    maps: dict[str, tuple[str, list[tuple[int, int, int]]]] = {}
    for line in lines:
        if line.startswith("seeds:"):
            seeds = line.split(": ")[1]
            vals = tuple(int(n) for n in seeds.split())
            maps["start"] = ("seeds", vals)
            continue
        if "-to-" in line:
            section, target = line.split()[0].split("-to-")
            maps[section] = (target, [])
            continue
        if line:
            vals = tuple(int(n) for n in line.split())
            assert len(vals) == 3
            maps[section][1].append(vals)
    # pprint(maps)
    return maps


def convert(seeds: list[int], mappings: list[tuple[int, int, int]]) -> list[int]:
    converted: list[int] = []
    for seed in seeds:
        for b, a, length in mappings:
            if a <= seed <= a + length:
                converted.append(b + seed - a)
                break
        else:
            # No map, keep same value
            converted.append(seed)

    return converted


def part1(input: list[str]) -> int:
    maps = parse(input)
    seeds = maps["start"][1]
    section = "seed"
    while section != "location":
        section, mappings = maps[section]
        seeds = convert(seeds, mappings)
        # print(seeds)
    return min(seeds)


assert part1(TEST_DATA) == EXPECTED

input = Path("input/day5.txt").read_text().splitlines()
print(part1(input))
# 836040384


def convert2(
    seeds: list[tuple[int, int]], mappings: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    converted: list[tuple[int, int]] = []
    for seed, slength in seeds:
        for b, a, length in mappings:
            if a <= seed < a + length:
                converted.append((b + seed - a, min(length, slength)))
                if slength > length:
                    seeds.append((seed + length, slength - length))
                    # print(f"New seed {seeds[-1]}")
                # print(f"{seed}, {slength} -> {converted[-1]}")
                break
            elif seed <= a and a < seed + slength:
                # print("split", seed, slength, a, length)
                seeds.append((seed, a - seed))
                slength -= a - seed
                seed = a
                converted.append((b, min(length, slength)))
                if slength > length:
                    seeds.append((seed + length, slength - length))
                break
        else:
            # No map, keep same value
            converted.append((seed, slength))
            # print(f"{seed}, {slength} -> {converted[-1]}")

    return converted


def part2(input: list[str]) -> int:
    maps = parse(input)
    seeds = list(pairwise(maps["start"][1]))[::2]
    section = "seed"
    while section != "location":
        section, mappings = maps[section]
        seeds = convert2(seeds, mappings)
    return min(s[0] for s in seeds)


EXPECTED2 = 46

assert part2(TEST_DATA) == EXPECTED2
print(part2(input))

# <37329216
# 10834440

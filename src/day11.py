from pathlib import Path

input = Path("input/day11.txt").read_text().splitlines()


TEST_DATA = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()
EXPECTED = 374


def parse(input: list[str]) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []
    for y, line in enumerate(input):
        x = line.find("#")
        while x >= 0:
            galaxies.append((x, y))
            x = line.find("#", x + 1)
    return galaxies


def empty_rows(galaxies: list[tuple[int, int]]) -> list[int]:
    rows = {y for x, y in galaxies}
    max_row = max(rows)
    return [i for i in range(0, max_row) if i not in rows]


def empty_cols(galaxies: list[tuple[int, int]]) -> list[int]:
    cols = {x for x, y in galaxies}
    max_col = max(cols)
    return [i for i in range(0, max_col) if i not in cols]


def expand(galaxies: list[tuple[int, int]], expansion: int) -> list[tuple[int, int]]:
    print(empty_cols(galaxies))
    exp = galaxies
    for row in empty_rows(galaxies)[::-1]:
        exp = [
            (g[0], g[1]) if orig[1] < row else (g[0], g[1] + expansion)
            for g, orig in zip(exp, galaxies)
        ]
    for col in empty_cols(galaxies)[::-1]:
        exp = [
            (g[0], g[1]) if orig[0] < col else (g[0] + expansion, g[1])
            for g, orig in zip(exp, galaxies)
        ]
    return exp


def part1(input: list[str], expansion: int = 2) -> int:
    galaxies = parse(input)
    # print(galaxies)
    galaxies = expand(galaxies, expansion - 1)
    # print(galaxies)
    pairs = [
        (galaxy, other)
        for n, galaxy in enumerate(galaxies, start=1)
        for other in galaxies[n:]
    ]
    distances = [
        max(galaxy[0], other[0])
        - min(galaxy[0], other[0])
        + max(galaxy[1], other[1])
        - min(galaxy[1], other[1])
        for galaxy, other in pairs
    ]
    # print(*[f"{p} -> {d}\n" for p,d in zip(pairs, distances)])
    return sum(distances)


res = part1(TEST_DATA)
print(res)
assert res == EXPECTED

# print(part1(input)) # 10494813

# print(part1(TEST_DATA, 10))
assert part1(TEST_DATA, 10) == 1030
assert part1(TEST_DATA, 100) == 8410
print(part1(input, 1_000_000))  # 840988812853

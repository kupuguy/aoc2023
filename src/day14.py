from pathlib import Path

input = Path("input/day14.txt").read_text().splitlines()

TEST_DATA = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".splitlines()

EXPECTED = 136


def parse(input: list[str]) -> tuple[int, list[list[tuple[int, str]]]]:
    top = len(input)
    grid: list[list[tuple[int, str]]] = [[] for i in range(len(input[0]))]
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c in ("O#"):
                grid[x].append((top - y, c))
    return top, grid


def shift_north(top: int, grid: list[list[tuple[int, str]]]):
    shifted: list[list[tuple[int, str]]] = []

    for col in grid:
        shifted.append([])
        prev = top + 1
        for n, c in col:
            if c == "O":
                prev -= 1
                shifted[-1].append((prev, c))
            else:
                shifted[-1].append((n, c))
                prev = n
    return shifted


def part1(input: list[str]) -> int:
    top, grid = parse(input)
    # print(top, grid)
    grid = shift_north(top, grid)
    # print(grid)
    return sum(n for col in grid for n, c in col if c == "O")


res = part1(TEST_DATA)
assert res == EXPECTED

print(part1(input))


def shift_west(top: int, grid: list[list[tuple[int, str]]]):
    width = len(grid)
    left_free = [-1 for i in range(top + 1)]
    shifted: list[list[tuple[int, str]]] = [[] for n in range(width)]

    for x, col in enumerate(grid):
        for n, c in col:
            if c == "O":
                left_free[n] += 1
                try:
                    shifted[left_free[n]].append((n, c))
                except IndexError:
                    print(x, n, c, len(left_free), left_free[n], len(shifted))
                    print(col)
                    exit()
            else:
                shifted[x].append((n, c))
                left_free[n] = x
    return [sorted(col, reverse=True) for col in shifted]


def shift_south(top: int, grid: list[list[tuple[int, str]]]):
    shifted: list[list[tuple[int, str]]] = []

    for col in grid:
        shifted.append([])
        prev = 0
        for n, c in col[::-1]:
            if c == "O":
                prev += 1
                shifted[-1].append((prev, c))
            else:
                shifted[-1].append((n, c))
                prev = n
    return [col[::-1] for col in shifted]


def shift_east(top: int, grid: list[list[tuple[int, str]]]):
    width = len(grid)
    right_free = [width for i in range(top + 1)]
    shifted: list[list[tuple[int, str]]] = [[] for n in range(width)]

    for x, col in reversed(list(enumerate(grid))):
        for n, c in col:
            if c == "O":
                right_free[n] -= 1
                shifted[right_free[n]].append((n, c))
            else:
                shifted[x].append((n, c))
                right_free[n] = x
    return [sorted(col, reverse=True) for col in shifted]


def show(top: int, grid: list[list[tuple[int, str]]]):
    matrix = [["."] * top for n in range(len(grid))]
    for x, col in enumerate(grid):
        for n, c in col:
            if matrix[x][n - 1] == ".":
                matrix[x][n - 1] = c
            else:
                matrix[x][n - 1] = "!"

    for line in reversed(list(zip(*matrix))):
        print("".join(line))
    print()


def validate(top: int, grid: list[list[tuple[int, str]]], orig) -> None:
    for x, col in enumerate(grid):
        p = top + 1
        for n, c in col:
            if not (1 <= n <= top) and n < p:
                show(top, grid)
                print(orig[x])
                print(col)
                print(n, c)
                raise RuntimeError()
            p = n


def spin(top: int, grid: list[list[tuple[int, str]]]):
    orig = grid
    validate(top, grid, orig)
    grid = shift_north(top, grid)
    validate(top, grid, orig)
    grid = shift_west(top, grid)
    validate(top, grid, orig)
    grid = shift_south(top, grid)
    validate(top, grid, orig)
    grid = shift_east(top, grid)
    validate(top, grid, orig)
    return grid


def grid_key(grid: list[list[tuple[int, str]]]) -> tuple[tuple[int]]:
    return tuple(tuple(n for n, c in col if c == "O") for col in grid)


def grid_score(grid: list[list[tuple[int, str]]]) -> int:
    return sum(n for col in grid for n, c in col if c == "O")


def part2(input: list[str], cycles: int) -> int:
    top, grid = parse(input)
    states = {grid_key(grid): (0, grid_score(grid))}
    # print(top, grid)
    turn = 1
    while True:
        grid = spin(top, grid)
        key = grid_key(grid)
        if key in states:
            start, score = states[key]
            print(f"State {start} repeats at {turn}")
            wanted = (cycles - start) % (turn - start) + start
            for n, score in states.values():
                if n == wanted:
                    return score
            raise RuntimeError()
        else:
            states[key] = (turn, grid_score(grid))
            turn += 1
    print(grid)
    return grid_score(grid)


CYCLES = 1_000_000_000
res = part2(TEST_DATA, CYCLES)
assert res == 64
print(part2(input, CYCLES))
# 100531

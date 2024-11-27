from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from string import ascii_uppercase

input = Path("input/day22.txt").read_text().strip().splitlines()

TEST_DATA = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""".splitlines()

EXPECTED = 5


@dataclass(unsafe_hash=True, eq=True)
class Block:
    name: str
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int
    supported_by: set("Block") = field(
        default_factory=set, init=False, hash=False, repr=False
    )
    supports: set("Block") = field(
        default_factory=set, init=False, hash=False, repr=False
    )

    def add_to_grid(self, grid: list[list["Block"]]):
        zmin = max(
            grid[y][x].z2
            for y in range(self.y1, self.y2 + 1)
            for x in range(self.x1, self.x2 + 1)
        )
        drop = self.z1 - zmin - 1
        if drop:
            self.z1 = zmin + 1
            self.z2 -= drop

        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                if grid[y][x].z2 == self.z1 - 1:
                    grid[y][x].supports.add(self)
                    self.supported_by.add(grid[y][x])
                grid[y][x] = self

    def can_disintegrate(self):
        return all(len(b.supported_by) > 1 for b in self.supports)

    @cache
    def all_supported(self) -> set["Block"]:
        blocks: set["Block"] = self.supports.copy()
        for b in self.supports:
            blocks |= b.all_supported()
        return blocks

    @cache
    def would_fall(self, removed: set["Block"] | None = None) -> set["Block"]:
        blocks = self.all_supported()
        all_supported = sorted(blocks, key=lambda b: (b.z1, b.x1, b.y1))

        if removed is None:
            removed = {self}
        for b in all_supported:
            if not b.supported_by - removed:
                removed.add(b)
        return removed - {self}


def parse(input: list[str]) -> list[Block]:
    blocks: list[Block] = []
    for index, line in enumerate(input):
        a, _, b = line.partition("~")
        x1, y1, z1 = [int(s) for s in a.split(",")]
        x2, y2, z2 = [int(s) for s in b.split(",")]
        name = ascii_uppercase[index % 26]
        while index := index // 26:
            name += ascii_uppercase[index % 26]

        blocks.append(Block(name, x1, y1, z1, x2, y2, z2))
    blocks.sort(key=lambda b: (b.z1, b.x1, b.y1))
    return blocks


def part1(input: list[str]) -> int:
    blocks = parse(input)
    xmin = min([min([b.x1, b.x2]) for b in blocks])
    xmax = max([max([b.x1, b.x2]) for b in blocks]) + 1
    ymin = min([min([b.y1, b.y2]) for b in blocks])
    ymax = max([max([b.y1, b.y2]) for b in blocks]) + 1
    ground = Block("Ground", xmin, ymin, 0, xmax, ymax, 0)
    grid: list[list[Block]] = [[ground] * xmax for i in range(ymax)]

    for b in blocks:
        b.add_to_grid(grid)

    # for b in blocks:
    #     print(b, b.can_disintegrate(), [c.name for c in b.supports])
    return sum(1 if b.can_disintegrate() else 0 for b in blocks)


res = part1(TEST_DATA)
# print(res)
assert res == EXPECTED

print(f"{part1(input)=}")
# 468


def part2(input: list[str]) -> int:
    blocks = parse(input)
    xmin = min([min([b.x1, b.x2]) for b in blocks])
    xmax = max([max([b.x1, b.x2]) for b in blocks]) + 1
    ymin = min([min([b.y1, b.y2]) for b in blocks])
    ymax = max([max([b.y1, b.y2]) for b in blocks]) + 1
    ground = Block("Ground", xmin, ymin, 0, xmax, ymax, 0)
    grid: list[list[Block]] = [[ground] * xmax for i in range(ymax)]

    for b in blocks:
        b.add_to_grid(grid)

    return sum(len(b.would_fall()) for b in blocks)


res = part2(TEST_DATA)
assert res == 7
print(f"{part2(input)=}")
# 75358

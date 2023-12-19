from pathlib import Path
from typing import Sequence
from functools import cache
from pprint import pprint
from collections import deque
import re
from typing import Callable
from operator import lt, gt
from dataclasses import dataclass

input = Path("input/day19.txt").read_text().strip().splitlines()

TEST_DATA = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".splitlines()

EXPECTED = 19114


class Part:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self) -> str:
        return f"<Part x:{self.x} m:{self.m} a:{self.a} s:{self.s}>"


@dataclass
class PartRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def combos(self) -> int:
        return (
            (self.x[1] - self.x[0])
            * (self.m[1] - self.m[0])
            * (self.a[1] - self.a[0])
            * (self.s[1] - self.s[0])
        )

    def split(
        self, field: str, op: Callable, value: int
    ) -> tuple["PartRange|None", "PartRange|None"]:
        mn, mx = getattr(self, field)
        if op is lt:
            return (
                PartRange(**(self.__dict__ | {field: (mn, value)}))
                if mn < value
                else None,
                PartRange(**(self.__dict__ | {field: (value, mx)}))
                if value < mx
                else None,
            )
        else:
            return (
                PartRange(**(self.__dict__ | {field: (value + 1, mx)}))
                if mx > value + 1
                else None,
                PartRange(**(self.__dict__ | {field: (mn, value + 1)}))
                if value >= mn
                else None,
            )


class Workflow:
    def __init__(self, branches: list[tuple[str, str]], action: str) -> None:
        self.branches: list[tuple[str, Callable, int, str]] = []
        self.action = action
        for cond, action in branches:
            field, op, value = cond[0], cond[1], cond[2:]
            assert field in "xmas"
            assert op in "<>"
            self.branches.append((field, lt if op == "<" else gt, int(value), action))

    def step(self, part: Part) -> str:
        for field, op, value, action in self.branches:
            if op(getattr(part, field), value):
                return action
        return self.action

    def combinations(self, part: PartRange, workflows: dict[str, "Workflow"]):
        count = 0
        for field, op, value, action in self.branches:
            ptrue, pfalse = part.split(field, op, value)
            if ptrue is not None:
                if action == "A":
                    count += ptrue.combos()
                elif action != "R":
                    count += workflows[action].combinations(ptrue, workflows)
            if pfalse is None:
                return count
            part = pfalse

        if self.action == "A":
            return part.combos() + count
        elif self.action == "R":
            return count

        count += workflows[self.action].combinations(part, workflows)
        return count


def run(part: Part, workflows: dict[str, Workflow]) -> bool:
    state = "in"
    states = [state]
    while state not in "RA":
        state = workflows[state].step(part)
        states.append(state)
    # print(' -> '.join(states))
    return state == "A"


def parse(input: list[str]) -> tuple[dict[str, Workflow], list[Part]]:
    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []
    for line in input:
        if not line:
            continue
        if line.startswith("{"):
            p = [
                int(v)
                for v in (
                    line[1:-1]
                    .replace("x=", "")
                    .replace("m=", "")
                    .replace("a=", "")
                    .replace("s=", "")
                    .split(",")
                )
            ]
            x, m, a, s = p
            parts.append(Part(x=x, m=m, a=a, s=s))
            continue

        name, _, rest = line[:-1].partition("{")
        steps = rest.split(",")
        branches = [step.split(":") for step in steps[:-1]]
        workflows[name] = Workflow(branches, steps[-1])

    return workflows, parts


def part1(input: list[str]) -> int:
    workflows, parts = parse(input)
    # print(parts)
    accepted = [p for p in parts if run(p, workflows)]
    # pprint(accepted)
    return sum(p.x + p.m + p.a + p.s for p in accepted)


res = part1(TEST_DATA)
print(res)
assert res == EXPECTED
print(part1(input))  # 353046

EXPECTED2 = 167409079868000


def part2(input: list[str]) -> int:
    workflows, parts = parse(input)
    return workflows["in"].combinations(
        PartRange(x=(1, 4001), m=(1, 4001), a=(1, 4001), s=(1, 4001)), workflows
    )


res = part2(TEST_DATA)
print("Test", res)
assert res == EXPECTED2
print(f"{part2(input)=}")
# 125355665599537

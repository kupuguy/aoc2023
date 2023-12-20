from pathlib import Path
from typing import Sequence
from functools import cache
from pprint import pprint
from collections import deque
import re
from typing import Callable
from operator import lt, gt
from dataclasses import dataclass
from math import lcm

input = Path("input/day20.txt").read_text().strip().splitlines()

TEST_DATA = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()

EXPECTED = 11687500

PULSE_QUEUE: deque[tuple[str, str, bool]] = deque()
HI = 0
LO = 0
PUSHES = 0


class Module:
    inputs: list[str]
    outputs: list[str]
    last_pulse: bool = True

    def __init__(self, name: str, outputs: list[str], inputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs
        self.inputs = inputs

    def send(self, pulse: bool):
        global LO, HI
        for n in self.outputs:
            PULSE_QUEUE.append((self.name, n, pulse))
            # print(f"{self.name} -{'high' if pulse else 'low'}-> {n}")
        if pulse:
            HI += len(self.outputs)
        else:
            LO += len(self.outputs)

    def receive(self, source: str, pulse: bool):
        self.last_pulse = pulse
        if not pulse and self.name == "rx":
            print(f"{self.name} got low after {PUSHES}")
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.name} -> {','.join(self.outputs)}"


class Broadcast(Module):
    def receive(self, source: str, pulse: bool):
        self.send(pulse)


class Flipflop(Module):
    state: bool = False

    def receive(self, source: str, pulse: bool):
        if not pulse:
            self.state = not self.state
            self.send(self.state)


class Conjunction(Module):
    state: dict[str, bool]

    def __init__(self, name: str, outputs: list[str], inputs: list[str]) -> None:
        super().__init__(name, outputs, inputs)
        self.state = {n: False for n in inputs}
        self.input_cycle = {}

    def receive(self, source: str, pulse: bool) -> None:
        # -- part 2 --
        if self.name == "tj":
            if pulse and source not in self.input_cycle:
                self.input_cycle[source] = PUSHES
        # -- end part 2 --

        self.state[source] = pulse
        self.send(not all(self.state.values()))


def run(modules: dict[str, Module]) -> None:
    global HI, LO
    PULSE_QUEUE.append(("button", "broadcaster", False))
    LO += 1
    while PULSE_QUEUE:
        source, targ, pulse = PULSE_QUEUE.popleft()
        modules[targ].receive(source, pulse)


def parse(input: list[str]) -> dict[str, Module]:
    out: dict[str, list[str]] = {}
    inp: dict[str, list[str]] = {"broadcaster": ["button"]}
    mtypes: dict[str, type[Module]] = {}
    for line in input:
        name, _, outputs = line.partition(" ->")
        if name.startswith("%"):
            name = name[1:]
            mtypes[name] = Flipflop
        elif name.startswith("&"):
            name = name[1:]
            mtypes[name] = Conjunction
        elif name == "broadcaster":
            mtypes[name] = Broadcast
        else:
            raise RuntimeError("oops")

        targets = out[name] = [n.strip() for n in outputs.strip().split(",")]
        for targ in targets:
            if targ in inp:
                inp[targ].append(name)
            else:
                inp[targ] = [name]
            if targ not in mtypes:
                mtypes[targ] = Module
                out[targ] = []

    return {name: mtypes[name](name, out[name], inp[name]) for name in mtypes}


def part1(input: list[str], pushes: int = 1000) -> int:
    global HI, LO, PUSHES
    HI, LO = 0, 0
    PUSHES = 0
    modules = parse(input)
    for push in range(pushes):
        PUSHES += 1
        run(modules)
        # print(HI, LO)
        # print()
    return HI * LO


res = part1(TEST_DATA)
assert res == EXPECTED
print(part1(input))  # 818649769


def part2(input: list[str], pushes: int = 10_000) -> int:
    global HI, LO, PUSHES
    HI, LO = 0, 0
    PUSHES = 0
    modules = parse(input)
    pprint(modules)
    for push in range(pushes):
        PUSHES += 1
        run(modules)
        tj = modules["tj"]
        if len(tj.input_cycle) == len(tj.inputs):
            return lcm(*tj.input_cycle.values())

    return HI * LO


print(f"{part2(input)=}")
# 246313604784977

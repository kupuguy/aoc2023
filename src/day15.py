from pathlib import Path

input = Path("input/day15.txt").read_text().strip()

TEST_DATA = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

EXPECTED = 1320


def hash_alg(s: str) -> int:
    code = 0
    for c in s:
        code = (code + ord(c)) * 17 % 256
    return code


assert hash_alg("HASH") == 52


def part1(steps: str) -> int:
    return sum(hash_alg(s) for s in steps.split(","))


assert part1(TEST_DATA) == EXPECTED
print(part1(input))


def focus_power(hashmap: dict[int, dict[str, int]]) -> int:
    power = 0
    for boxno, slot in enumerate(hashmap.values(), start=1):
        for slot, pwr in enumerate(slot.values(), start=1):
            print(boxno, slot, pwr)
            power += boxno * slot * pwr
    return power


def part2(steps: str) -> int:
    hashmap: dict[int, dict[str, int]] = {n: {} for n in range(256)}
    for step in steps.split(","):
        # print(step)
        if step.endswith("-"):
            label = step[:-1]
            n = hash_alg(label)
            # print(n, label, label in hashmap[n])
            if label in hashmap[n]:
                del hashmap[n][label]
        else:
            label, pwr = step.split("=")
            n = hash_alg(label)
            hashmap[n][label] = int(pwr)
    print(*[hashmap[k] for k in hashmap if hashmap[k]], sep="\n")
    return focus_power(hashmap)


res = part2(TEST_DATA)
assert res == 145
print(part2(input))

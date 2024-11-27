from pathlib import Path

import networkx as nx

input = Path("input/day25.txt").read_text().strip().splitlines()

TEST_DATA = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines()

EXPECTED = 54


def parse(input: list[str]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for line in input:
        node, _, rest = line.partition(": ")
        others = rest.split()
        graph[node] = others
    print(f"{len(graph)} nodes, {sum(len(s) for s in graph.values())} links")
    return graph


# How do I find communities in a graph? Google said use networkx so I did.
# Oh, that was rather easier than I'd expected! It even used the parse code
# I'd already written.
def part1(input: list[str]) -> int:
    graph = nx.Graph(parse(input))
    print(graph)
    comp = nx.community.girvan_newman(graph)
    c1, c2 = tuple(sorted(c) for c in next(comp))
    return len(c1) * len(c2)


res = part1(TEST_DATA)
assert res == EXPECTED
print(f"{part1(input)=}")

# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re
import networkx as nx

puz = Puzzle(year=2022, day=16)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\nValve BB has flow rate=13; tunnels lead to valves CC, AA\nValve CC has flow rate=2; tunnels lead to valves DD, BB\nValve DD has flow rate=20; tunnels lead to valves CC, AA, EE\nValve EE has flow rate=3; tunnels lead to valves FF, DD\nValve FF has flow rate=0; tunnels lead to valves EE, GG\nValve GG has flow rate=0; tunnels lead to valves FF, HH\nValve HH has flow rate=22; tunnel leads to valve GG\nValve II has flow rate=0; tunnels lead to valves AA, JJ\nValve JJ has flow rate=21; tunnel leads to valve II"
# D B J H E C
TEST_RESULT_A = 1651
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    info = {}
    start = None
    for line in data.split("\n"):
        vstring, tstring = line.split("; ")
        node, fr = re.findall(r"\s([A-Z]{2})\s.+(\=\d+)", vstring)[0]
        edges = re.findall(r"([A-Z]{2})", tstring)
        info[node] = (int(fr[1:]), edges)
        if start is None:
            start = node
    return info, start


def make_graph(info):
    g = nx.Graph({k: tuple(v[1]) for k, v in info.items()})
    for k, v in info.items():
        g.nodes[k]["fr"] = v[0]
    return g


def main1(data=None):
    info, start = format_data(data)
    current = start
    opened = []
    g = make_graph(info)
    targets = list(
        sorted([(v[0], k) for k, v in info.items() if v[0] > 0], reverse=True)
    )
    time = 30
    total_flow = 0
    while time > 0:
        if current not in opened and info[current][0] > 0:
            time -= 1
            total_flow += info[current][0] * time
            opened.append(current)
            targets.remove((info[current][0], current))
        if len(targets) > 0:
            shortest_paths = [
                (t[0], nx.shortest_path(g, current, t[1])) for t in targets
            ]
            weighted_paths = list(
                sorted(
                    [((time - len(p)) * fr, p) for fr, p in shortest_paths],
                    reverse=True,
                )
            )
            _, path = weighted_paths[0]
            if len(path) > 1:
                for i, p in enumerate(path[1:]):
                    if info[p][0] > 0:
                        current = p
                        time -= i + 1
        else:
            time -= 1
    print(total_flow)
    return total_flow


def main2(data=None):
    pass


assert main1(TEST_DATA_A) == TEST_RESULT_A
# resa = main1(puz.input_data)
# print(f'solution: {resa}')
# puz.answer_a = resa

assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

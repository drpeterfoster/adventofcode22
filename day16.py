# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re
import networkx as nx
from itertools import permutations

# puz = Puzzle(year=2022, day=16)
# print(puz.url)

# puz.input_data

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
    g = nx.Graph({k: tuple(v[1]) for k, v in info.items()})
    for k, v in info.items():
        g.nodes[k]["fr"] = v[0]
    return g, start

def adj_time(t, p):
    return t - len(p) - 1  # time to get there and turn the switch

def main1(data=None, n=3):
    g, start = format_data(data)
    # get list of nodes to visit
    node2fr = {n: d['fr'] for n, d in g.nodes(data=True) if d['fr'] > 0}
    targets = list(node2fr.keys())
    path = [start]
    if start in targets:
        targets.remove(start)
    paths = [(targets.copy(), path, 30, 0)]
    if node2fr.get(start, 0) > 0:
        paths.append((targets.copy(), path, 29, node2fr[start]*29))
    
    for i in range(len(targets)):
        newpaths = []
        for _targets, _path, _time, _tf in paths:
            # [paths]
            shortpaths = [nx.shortest_path(g, _path[-1], target) for target in _targets]
            # [(total_val, path)]
            valuepaths = list(sorted([(adj_time(_time, p) * node2fr[p[-1]], p) for p in shortpaths], reverse=True))
            for _, p in valuepaths[:min(len(valuepaths), n)]:
                _newtargets = [x for x in _targets if x != p[-1]]
                _newpath = _path.copy() + [p[-1]]
                _newtime = adj_time(_time, p)
                _newtf = _tf + adj_time(_time, p)* node2fr[p[-1]]
                newpaths.append((_newtargets, _newpath, _newtime, _newtf))
        newpaths = list(sorted(newpaths, key=lambda x: x[3], reverse=True))
        paths = newpaths[:min(len(newpaths), n**2)].copy()
    _, chosen_path, _, answer = paths[0]
    print(chosen_path, answer)
    return answer


def main2(data=None):
    pass


assert main1(TEST_DATA_A, 1000000) == TEST_RESULT_A
# resa = main1(puz.input_data)
# print(f'solution: {resa}')
# puz.answer_a = resa

assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

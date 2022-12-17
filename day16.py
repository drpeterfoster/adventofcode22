# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re
import networkx as nx
from itertools import combinations, permutations

puz = Puzzle(year=2022, day=16)
print(puz.url)

# puz.input_data

TEST_DATA_A = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\nValve BB has flow rate=13; tunnels lead to valves CC, AA\nValve CC has flow rate=2; tunnels lead to valves DD, BB\nValve DD has flow rate=20; tunnels lead to valves CC, AA, EE\nValve EE has flow rate=3; tunnels lead to valves FF, DD\nValve FF has flow rate=0; tunnels lead to valves EE, GG\nValve GG has flow rate=0; tunnels lead to valves FF, HH\nValve HH has flow rate=22; tunnel leads to valve GG\nValve II has flow rate=0; tunnels lead to valves AA, JJ\nValve JJ has flow rate=21; tunnel leads to valve II"
# D B J H E C
TEST_RESULT_A = 1651
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    graph = {}
    node2fr = {}
    start = None
    for line in data.split("\n"):
        vstring, tstring = line.split("; ")
        node, fr = re.findall(r"\s([A-Z]{2})\s.+(\=\d+)", vstring)[0]
        edges = re.findall(r"([A-Z]{2})", tstring)
        graph[node] = tuple(edges)
        node2fr[node] = int(fr[1:])
        if start is None:
            start = node
    g0 = nx.Graph(graph)
    targets = set([k for k, v in node2fr.items() if v > 0]).union([start])
    elist = [
        (a, b, len(nx.shortest_path(g0, a, b)) - 1) for a, b in combinations(targets, 2)
    ]
    g = nx.Graph()
    g.add_weighted_edges_from(elist)
    for n in g.nodes:
        g.nodes[n]["fr"] = node2fr[n]
    return g, start


def dfexplore(g, start, sibs, path, bestpath):
    if start not in path:
        path.append(start)
    if start in sibs:
        sibs.remove(start)
    neighbors = [n for n in g.neighbors(start) if n not in path]
    for n in neighbors:
        sibs, path, bestpath = dfexplore(g, n, neighbors, path, bestpath)
    score = score_path(g, path)
    if score > bestpath[0]:
        bestpath = (score, path)
    # step up, over, & continue search
    if len(sibs) > 0:
        newstart = sibs[0]
        path.pop()
        neighbors = [n for n in g.neighbors(newstart) if n not in path]
        sibs, path, bestpath = dfexplore(g, sibs[0], neighbors, path, bestpath)
    return sibs, path, bestpath


def score_path(g, path):
    time = 30
    tf = 0
    if g.nodes[path[0]]["fr"] > 0:
        time -= 1
        tf += g.nodes[path[0]]["fr"] * time
    for i in range(len(path) - 1):
        time -= g.edges[(path[i], path[i + 1])]["weight"] + 1
        if time < 0:
            break
        tf += g.nodes[path[i + 1]]["fr"] * time
    return tf


def main1(data):
    g, start = format_data(data)
    search_nodes = list(g.nodes)
    search_nodes.remove(start)
    answer = 0
    for path in permutations(search_nodes):
        score = score_path(g, [start] + list(path))
        if score > answer:
            answer = score
    print(answer)
    return answer


def main1_deprecated2(data):
    g, start = format_data(TEST_DATA_A)
    bestpath = (0, [])
    starting_neighbors = [n for n in g.neighbors(start)]
    _, _, bestpath = dfexplore(g, start, starting_neighbors, [start], bestpath)
    print(bestpath)
    return bestpath[0]


def main1_deprecated1(data=None, n=3):
    def adj_time(t, p):
        return t - len(p)  # time to get there and turn the switch

    g, start = format_data(data)
    # get list of nodes to visit
    node2fr = {n: d["fr"] for n, d in g.nodes(data=True) if d["fr"] > 0}
    targets = list(node2fr.keys())
    path = [start]
    if start in targets:
        targets.remove(start)
    paths = [(targets.copy(), path, 30, 0)]
    if node2fr.get(start, 0) > 0:
        paths.append((targets.copy(), path, 29, node2fr[start] * 29))
    print(len(targets))
    for i in range(len(targets)):
        newpaths = []
        for _targets, _path, _time, _tf in paths:
            # [paths]
            shortpaths = [nx.shortest_path(g, _path[-1], target) for target in _targets]
            # [(total_val, path)]
            valuepaths = list(
                sorted(
                    [(adj_time(_time, p) * node2fr[p[-1]], p) for p in shortpaths],
                    reverse=True,
                )
            )
            for _, p in valuepaths[: min(len(valuepaths), n)]:
                _newtargets = [x for x in _targets if x != p[-1]]
                _newpath = _path.copy() + [p[-1]]
                _newtime = adj_time(_time, p)
                _newtf = _tf + adj_time(_time, p) * node2fr[p[-1]]
                if _newtf > 0:
                    newpaths.append((_newtargets, _newpath, _newtime, _newtf))
        newpaths = list(sorted(newpaths, key=lambda x: x[3], reverse=True))
        paths = newpaths[: min(len(newpaths), n**2)].copy()
        print(i, len(paths), end="; ")
    _, chosen_path, _, answer = paths[0]
    return answer


def main2(data=None):
    pass


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

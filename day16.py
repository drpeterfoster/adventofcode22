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
TEST_RESULT_B = 1707


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


#%%
def dfexplore(g, start, path, bestpath):
    if start not in path:
        path.append(start)
        neighbors = [n for n in g.neighbors(start) if n not in path]
        if not len(neighbors):
            score = score_path(g, path)
            if score > bestpath[0]:
                bestpath = (score, path)
        # check if worth continuing
        # return path[:-1], bestpath
        while len(neighbors) > 0:
            n = neighbors.pop()
            path, bestpath = dfexplore(g, n, path, bestpath)
    return path[:-1], bestpath


# def time2bail(g, path, neighbors, bestpath):
#     # min value of all edge weights * len(neighbors)
#     curr_score = score_path(g, path)


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


def main1_permuteall(data):
    g, start = format_data(data)
    search_nodes = list(g.nodes)
    search_nodes.remove(start)
    answer = 0
    for path in permutations(search_nodes):
        score = score_path(g, [start] + list(path))
        if score > answer:
            answer = score
    return answer


def main1_dfs(data):
    g, start = format_data(TEST_DATA_A)
    bestpath = (0, [])
    _, bestpath = dfexplore(g, start, [], bestpath)
    return bestpath[0]


def main1_sortedstep(data=None, n=3):
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
    # print(len(targets))
    for i in range(len(targets)):
        newpaths = []
        for _targets, _path, _time, _tf in paths:
            valpaths = []
            for _, b, d in g.edges(_path[-1], data=True):
                if b not in _path:
                    _newtargets = [x for x in _targets if x != b]
                    _newtime = _time - d["weight"] - 1
                    _newtf = _tf + g.nodes[b]["fr"] * _newtime
                    _newpath = _path.copy() + [b]
                    if _newtf > 0:
                        newpaths.append((_newtargets, _newpath, _newtime, _newtf))
        newpaths = list(sorted(newpaths, key=lambda x: x[3], reverse=True))
        paths = newpaths[: min(len(newpaths), n**2)].copy()
        # print(i, len(paths), end='; ')
    _, chosen_path, _, answer = paths[0]
    # print(answer)
    return answer


def main1_beststep(data):
    g, start = format_data(data)
    time = 30
    tf = 0
    path = [start]
    if g.nodes[start]["fr"] > 0:
        time -= 1
        tf += g.nodes[start]["fr"] * time
    while set(path) != set(g.nodes):
        stepvals = []
        for _, b, d in g.edges(path[-1], data=True):
            if b not in path:
                _t = time - d["weight"] - 1
                _tf = tf + g.nodes[b]["fr"] * _t
                _path = path.copy() + [b]
                stepvals.append((_tf, _t, _path))
        tf, time, path = list(sorted(stepvals, reverse=True))[0]
        print(tf, time, path)
    print(tf)
    return tf


def main2(data=None):
    pass


assert main1_permuteall(TEST_DATA_A) == TEST_RESULT_A
assert main1_dfs(TEST_DATA_A) == TEST_RESULT_A
# assert main1_beststep(TEST_DATA_A) == TEST_RESULT_A  # doesn't work
assert main1_sortedstep(TEST_DATA_A, 3) == TEST_RESULT_A
# resa = main1_sortedstep(puz.input_data, 500)
resa = main1_dfs(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main1_dfs(TEST_DATA_A, 2) == TEST_RESULT_B
# resb = main2_dfs(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

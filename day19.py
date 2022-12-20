# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re
from copy import deepcopy

puz = Puzzle(year=2022, day=19)
print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\nBlueprint 2:Each ore robot costs 2 ore.Each clay robot costs 3 ore.Each obsidian robot costs 3 ore and 8 clay.Each geode robot costs 3 ore and 12 obsidian."
TEST_RESULT_A = 33
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    info = {}
    for line in data.split("\n"):
        bp, orob, crob, orobo, orobc, grobo, grobb = map(int, re.findall(r"\d+", line))
        info[bp] = {
            "ore": {"ore": orob},
            "clay": {"ore": crob},
            "obs": {"ore": orobo, "clay": orobc},
            "geo": {"ore": grobo, "obs": grobb},
        }
    return info


def can_build(robot, inv, costs):
    return all([inv[resource] >= cost for resource, cost in costs[robot].items()])


def greedy_orders(robs, inv, costs):
    """Doesn't work... but simple enough to try first."""
    newrobs = {k: 0 for k in robs.keys()}
    for robot in "geo obs clay ore".split():
        if can_build(robot, inv, costs):
            newrobs[robot] += 1
            for resource, n in costs[robot].items():
                inv[resource] -= n
    return newrobs, inv


def update_inventory(inv, robs):
    for rob, n in robs.items():
        inv[rob] += n
    return inv


def update_robots(robs, newrobs):
    for rob, n in newrobs.items():
        robs[rob] += n
    return robs


def main1_greedy(data=None):
    bps = format_data(data)
    bp_geodes = {}
    for bpi, costs in bps.items():
        inv = dict(ore=0, clay=0, obs=0, geo=0)
        robs = dict(ore=1, clay=0, obs=0, geo=0)
        for i in range(1, 25):  # fixed time range
            newrobs, inv = greedy_orders(robs, inv, costs)
            inv = update_inventory(inv, robs)
            robs = update_robots(robs, newrobs)
        bp_geodes[bpi] = inv["geo"]
    answer = sum([np.product(x, dtype=int) for x in bp_geodes.items()])
    print(bp_geodes)
    print(answer)
    return answer


def plausible_orders(orders, bestorders):
    best = [i for i, b in bestorders if b == "clay"]
    first = [i for i, b in orders if b == "clay"]
    if len(best) > 0 and len(first) > 0 and first[0] > best[0]:
        return False
    best = [i for i, b in bestorders if b == "obs"]
    first = [i for i, b in orders if b == "obs"]
    if len(best) > 0 and len(first) > 0 and first[0] > best[0]:
        return False
    best = [i for i, b in bestorders if b == "geo"]
    first = [i for i, b in orders if b == "geo"]
    if len(best) > 0 and len(first) > 0 and first[0] > best[0]:
        return False
    return True


def tree_search(inv, robs, i, orders, bestorders, stack, costs):
    newstates = []
    if i < 24:  # returns nothing, just adds states to stack
        i += 1
        # if state can afford any robot, skip no op
        if not all([can_build(robot, inv, costs) for robot in robs.keys()]):
            newstates += [(deepcopy(inv), deepcopy(robs), i, deepcopy(orders))]  # no op
        # get & execute all possible orders, add to stack
        for robot in "geo obs clay ore".split():
            if can_build(robot, inv, costs):
                newrobs, newinv, neworders = (
                    deepcopy(robs),
                    deepcopy(inv),
                    deepcopy(orders),
                )
                newrobs[robot] += 1
                neworders += [(i, robot)]
                for resource, n in costs[robot].items():
                    newinv[resource] -= n
                newstates += [(newinv, newrobs, i, neworders)]  # executed
        # update inventories (based on input state)
        for _inv, _, _, _ in newstates:
            update_inventory(_inv, robs)
        stack += [
            state for state in newstates if plausible_orders(state[-1], bestorders)
        ]
        return ({}, {}, 0, [])
    else:  # when game is over, returns gamestate
        return (inv, robs, i, orders)


def main1_tree(data=None):
    """blegh. i think i need to be smarter about adding to the stack vs filtering crappy things out"""
    bps = format_data(data)
    bp_geodes = {}
    bp_bestorders = {}
    for bpi, costs in bps.items():
        bp_geodes[bpi] = 0
        bp_bestorders[bpi] = []
        inv = dict(ore=0, clay=0, obs=0, geo=0)
        robs = dict(ore=1, clay=0, obs=0, geo=0)
        stack = {i: [] for i in range(0, 25)}
        stack = [(inv, robs, 0, [])]
        counter = 0
        while len(stack) > 0:
            counter += 1
            ix = -1 if counter % 10 != 0 else 0
            _inv, _robs, _i, _orders = tree_search(
                *stack.pop(ix), bp_bestorders[bpi], stack, costs
            )
            if _inv.get("geo", 0) > bp_geodes[bpi]:
                bp_geodes[bpi] = _inv["geo"]
                bp_bestorders[bpi] = deepcopy(_orders)
            if counter % 1000 == 0:
                print(counter, len(stack), bp_geodes[bpi], bp_bestorders[bpi])
    answer = sum([np.product(x, dtype=int) for x in bp_geodes.items()])
    print(bp_geodes)
    print(answer)
    return answer


def main2(data=None):
    pass


assert main1_tree(TEST_DATA_A) == TEST_RESULT_A
# resa = main1(puz.input_data)
# print(f'solution: {resa}')
# puz.answer_a = resa

# assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

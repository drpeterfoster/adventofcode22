# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re
from copy import deepcopy
from queue import PriorityQueue
from dataclasses import dataclass, field
from tqdm import tqdm


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


def update_inventory(inv, robs):
    for rob, n in robs.items():
        inv[rob] += n
    return inv


def update_robots(robs, newrobs):
    for rob, n in newrobs.items():
        robs[rob] += n
    return robs


@dataclass
class State:
    inv: dict
    robs: dict
    t: int
    orders: list
    tgeo: dict = field(default_factory=dict)


def rank_state(state, costs, i=0):
    # cla max(ceil(crobs.o / orobs))
    t_cla = np.ceil((costs["clay"]["ore"] - state.inv["ore"]) / state.robs["ore"]) + 1
    # obs max(ceil(obrobs.c / crobs), ceil(grobs.o / orobs))
    t_obs = 1
    if state.robs["clay"] == 0:
        t_obs += t_cla
    t_obs += max(
        [
            np.ceil(
                (costs["obs"]["clay"] - state.inv["clay"]) / max(state.robs["clay"], 1)
            ),
            np.ceil((costs["obs"]["ore"] - state.inv["ore"]) / state.robs["ore"]),
        ]
    )
    # geo max(ceil(grobs.obs / obrobs ), ceil(grobs.o / orobs))
    t_geo = 1
    if state.robs["obs"] == 0:
        t_geo += t_obs
    t_geo += max(
        [
            np.ceil(
                (costs["geo"]["obs"] - state.inv["obs"]) / max(state.robs["obs"], 1)
            ),
            np.ceil((costs["geo"]["ore"] - state.inv["ore"]) / state.robs["ore"]),
        ]
    )
    t_geo += 1  # index offset
    state.tgeo[state.t] = state.robs["geo"], int(t_geo)
    return int(t_geo), int(t_geo + state.t), i, state


"""
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.
  
      01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 

2 ore 06 08 10 12 14 16 18 20 22
3 cla 03 06 09 12 15 18 21
1 obs 01 02 03 04 05 06 07 01                    
1 geo                         01                                                       01 02                                
"""

STATE1 = State(
    dict(ore=0, clay=0, obs=0, geo=0), dict(ore=1, clay=0, obs=0, geo=0), 0, []
)  # 27
STATE2 = State(
    dict(ore=0, clay=0, obs=0, geo=0), dict(ore=1, clay=0, obs=0, geo=0), 1, []
)  # 27
STATE3 = State(
    dict(ore=0, clay=0, obs=0, geo=0), dict(ore=1, clay=1, obs=0, geo=0), 3, []
)  # 24
STATE4 = State(
    dict(ore=0, clay=0, obs=0, geo=0), dict(ore=1, clay=1, obs=1, geo=0), 0, []
)  # 9
STATE5 = State(
    dict(ore=0, clay=0, obs=0, geo=1), dict(ore=1, clay=0, obs=0, geo=0), 0, []
)  # 27
STATE6 = State(
    dict(ore=2, clay=0, obs=0, geo=0), dict(ore=2, clay=3, obs=1, geo=0), 0, []
)  # 9


def test_rank_state(state):
    costs_dict = format_data(TEST_DATA_A)
    rank = rank_state(state, costs_dict[1], 0)
    print(rank[:-1])


# test_rank_state(STATE1)
# test_rank_state(STATE2)
# test_rank_state(STATE3)
# test_rank_state(STATE4)
# test_rank_state(STATE5)
# test_rank_state(STATE6)

# %%
def better_than_best(state, bestorders):
    bests = {bot: i for i, bot in bestorders[::-1]}
    firsts = {bot: i for i, bot in state.orders[::-1]}
    checks = []
    for bot in ["obs", "geo"]:
        best = bests.get(bot, None)
        first = firsts.get(bot, None)
        if best is not None:
            if first is not None:
                checks.append(first <= best)
            else:
                if state.t >= best:
                    checks.append(False)
                else:
                    checks.append(True)
        else:
            checks.append(True)
    return all(checks)


# def better_than_best(state, best_tgeos):
#     na = (0, np.inf)
#     return all(
#         [
#             tgeo[0] >= best_tgeos.get(turn, na)[0]
#             and tgeo[1] <= best_tgeos.get(turn, na)[1]+1
#             for turn, tgeo in state.tgeo.items()
#         ]
#     )


def next_states(state, costs):
    newstates = []
    if state.t < 24:
        i = state.t + 1
        # executed next states
        for robot in "geo obs clay ore".split():
            if can_build(robot, state.inv, costs):
                newstate = deepcopy(state)
                newstate.t = i
                newstate.orders += [(i, robot)]
                for resource, n in costs[robot].items():
                    newstate.inv[resource] -= n
                newstate.robs[robot] += 1
                update_inventory(newstate.inv, state.robs)
                newstates += [newstate]
        # no op
        max_ore = max([v.get("ore", 0) for v in costs.values()])
        max_clay = max([v.get("clay", 0) for v in costs.values()])
        if (
            not all([can_build(robot, state.inv, costs) for robot in state.robs.keys()])
            and state.inv["ore"] < 2 * max_ore
            and state.inv["clay"] < 2 * max_clay
        ):
            newstate = deepcopy(state)
            newstate.t = i
            update_inventory(newstate.inv, state.robs)
            newstates += [newstate]
    else:
        pass
    return newstates


def optimize_bp(costs):
    bestorders = []
    best_tgeos = {}
    most_geos = 0
    init_state = rank_state(
        State(
            inv=dict(ore=0, clay=0, obs=0, geo=0),
            robs=dict(ore=1, clay=0, obs=0, geo=0),
            t=0,
            orders=[],
        ),
        costs=costs,
        i=0,
    )
    stack = PriorityQueue()
    stack.put(init_state)
    i = 0
    while not stack.empty():
        rstate = stack.get()
        state = rstate[-1]
        if not better_than_best(state, bestorders):
            continue
        # if not better_than_best(state, best_tgeos):
        #     continue
        newstates = next_states(state, costs)
        for state in newstates:
            i += 1
            rstate = rank_state(state, costs, i)
            if state.t == 24 and state.inv["geo"] > most_geos:
                most_geos = state.inv["geo"]
                bestorders = deepcopy(state.orders)
                best_tgeos = deepcopy(state.tgeo)
            else:
                stack.put(rstate)
    return most_geos, bestorders


def main1(data):
    bps = format_data(data)
    bp_geodes = {}
    bp_bestorders = {}
    for bpi, costs in tqdm(bps.items()):
        bp_geodes[bpi], bp_bestorders[bpi] = optimize_bp(costs)
        print(bpi, bp_geodes[bpi])
    answer = sum([np.product(x, dtype=int) for x in bp_geodes.items()])
    print(answer)
    return answer


main1(TEST_DATA_A)
print(TEST_RESULT_A)

# assert main1_tree(TEST_DATA_A) == TEST_RESULT_A
# resa = main1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

# def main2(data=None):
#     pass

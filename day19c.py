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

TEST_DATA_A = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\nBlueprint 2:Each ore robot costs 2 ore.Each clay robot costs 3 ore.Each obsidian robot costs 3 ore and 8 clay.Each geode robot costs 3 ore and 12 obsidian."
TEST_RESULT_A = 33
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    info = {}
    for line in data.split("\n"):
        bp, orob, crob, orobo, orobc, grobo, grobb = map(int, re.findall(r"\d+", line))
        info[bp] = {
            "ore": np.array([orob, 0, 0, 0]),
            "clay": np.array([crob, 0, 0, 0]),
            "obs": np.array([orobo, orobc, 0, 0]),
            "geo": np.array([grobo, 0, grobb, 0]),
            "noop": np.array([0, 0, 0, 0]),
        }
    return info


@dataclass
class State:
    costs: dict
    inv: np.ndarray = np.array([0, 0, 0, 0])
    robs: np.ndarray = np.array([1, 0, 0, 0])
    t: int = 0
    prod: dict = field(
        default_factory=lambda: dict(
            ore=np.array([1, 0, 0, 0]),
            clay=np.array([0, 1, 0, 0]),
            obs=np.array([0, 0, 1, 0]),
            geo=np.array([0, 0, 0, 1]),
            noop=np.array([0, 0, 0, 0]),
        )
    )

    def can_build(self, robot):
        return np.all((self.inv - self.costs[robot]) >= 0)

    def buycollectbuild(self, robot, undo=False):
        if undo:
            self.t -= 1
            self.robs -= self.prod[robot]
            self.inv -= self.robs
            self.inv += self.costs[robot]
        else:
            self.t += 1
            self.inv -= self.costs[robot]
            self.inv += self.robs
            self.robs += self.prod[robot]
        return self

    def shouldbuild(self, robot):
        match robot:
            case "ore":
                return self.robs[0] <= max([costs[0] for costs in self.costs.values()])
            case "clay":
                return self.robs[1] <= max(
                    [costs[1] for costs in self.costs.values()]
                ) and self.robs[2] <= max([costs[2] for costs in self.costs.values()])
            case "obs":
                return self.robs[2] <= max([costs[2] for costs in self.costs.values()])
            case "geo":
                return True
            case "noop":
                return not all([self.can_build(bot) for bot in self.prod])


def solver(state, maxgeo):
    if state.t < 24:
        maxes = [maxgeo]
        canbuild = [rob for rob in state.prod if state.can_build(rob)]
        for newrob in canbuild:
            state.buycollectbuild(newrob)
            should = state.shouldbuild(newrob)
            if should:
                newmax = solver(state, max(maxes))
                maxes.append(newmax)
            state.buycollectbuild(newrob, undo=True)
            if newrob == "geo":
                break
        return max(maxes)
    return max([maxgeo, state.inv[-1]])


def main1(data):
    bps = format_data(data)
    bp_geodes = {i: 0 for i in range(1, len(bps) + 1)}
    bps.pop(1)
    for bpi, costs in tqdm(bps.items()):
        state = State(costs=costs)
        bp_geodes[bpi] = solver(state, bp_geodes[bpi])
        # print(bpi, bp_geodes[bpi])
    answer = int(sum([np.product(x, dtype=int) for x in bp_geodes.items()]))
    print(bp_geodes, answer)
    return answer


main1(TEST_DATA_A)
print(TEST_RESULT_A)

# resa = main1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

# resb = main2(puz.input_data, 32)
# print(f"solution: {resb}")
# puz.answer_b = resb
# %%

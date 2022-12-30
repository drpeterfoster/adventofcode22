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
            "noop": {},
            "ore": {"ore": orob},
            "clay": {"ore": crob},
            "obs": {"ore": orobo, "clay": orobc},
            "geo": {"ore": grobo, "obs": grobb},
        }
    return info


@dataclass
class State:
    inv: dict
    robs: dict
    t: int
    costs: dict
    buildtimes: list = field(
        default_factory=lambda: dict(clay=np.inf, obs=np.inf, geo=np.inf)
    )

    def copy(self):
        newinstance = State(
            inv=deepcopy(self.inv),
            robs=deepcopy(self.robs),
            t=self.t,
            costs=self.costs,
            buildtimes=deepcopy(self.buildtimes),
        )
        return newinstance

    def can_build(self, robot):
        return all(
            [self.inv[resource] >= cost for resource, cost in self.costs[robot].items()]
        )

    def build(self, robot):
        self.robs[robot] += 1
        for resource, n in self.costs[robot].items():
            self.inv[resource] -= n
        return self

    def update_inv(self, robs):
        for rob, n in robs.items():
            self.inv[rob] += n
        return self

    def time2next(self):
        t_cla = np.ceil(
            (self.costs["clay"]["ore"] - self.inv["ore"]) / self.robs["ore"]
        )
        if self.robs["clay"] == 0:
            t_obs = np.inf
        else:
            t_obs = max(
                [
                    np.ceil(
                        (self.costs["obs"]["clay"] - self.inv["clay"])
                        / self.robs["clay"]
                    ),
                    np.ceil(
                        (self.costs["obs"]["ore"] - self.inv["ore"]) / self.robs["ore"]
                    ),
                ]
            )
        if self.robs["obs"] == 0:
            t_geo = np.inf
        else:
            t_geo = max(
                [
                    np.ceil(
                        (self.costs["geo"]["obs"] - self.inv["obs"])
                        / max(self.robs["obs"], 1)
                    ),
                    np.ceil(
                        (self.costs["geo"]["ore"] - self.inv["ore"]) / self.robs["ore"]
                    ),
                ]
            )
        self.buildtimes = {"clay": t_cla + 1, "obs": t_obs + 1, "geo": t_geo + 1}
        return self

    def shouldbuild(self, oldstate, robot):
        func = lambda robs: [
            self.buildtimes[bot] + 1 <= oldstate.buildtimes[bot] for bot in robs
        ]
        match robot:
            case "ore":
                if self.robs[robot] > max(
                    [costs.get(robot, 0) for costs in self.costs.values()]
                ):
                    return False
                return any(func(["geo", "obs", "clay"]))
            case "clay":
                if (
                    self.robs[robot]
                    > max([costs.get(robot, 0) for costs in self.costs.values()]) / 2
                ):
                    return False
                return all(func(["geo", "obs"]))
            case "obs":
                return all(func(["geo"]))
            case "geo":
                return True
            case "noop":
                return all(func(["geo", "obs", "clay"]))


def solver(state, stack, maxgeo):
    if state.t < 24:
        canbuild = [rob for rob in state.robs if state.can_build(rob)]
        substack = []
        for newrob in "geo obs clay ore noop".split():
            if newrob not in canbuild:
                continue
            newstate = state.copy()
            newstate.t += 1
            newstate.build(newrob)
            newstate.update_inv(state.robs)
            newstate.time2next()
            should = newstate.shouldbuild(state, newrob)
            if should:
                substack.append(newstate)
            if newrob == "geo":
                break
        if len(substack) > 0:
            nextstate = substack.pop(0)
            stack += substack
            maybemax = solver(nextstate, stack, max([maxgeo, nextstate.inv["geo"]]))
        return max([maxgeo, maybemax])
    return maxgeo


def main1(data):
    bps = format_data(data)
    bp_geodes = {i: 0 for i in range(len(bps) + 1)}
    bps.pop(1)
    for bpi, costs in tqdm(bps.items()):
        init_state = State(
            inv=dict(ore=0, clay=0, obs=0, geo=0, noop=0),
            robs=dict(ore=1, clay=0, obs=0, geo=0, noop=0),
            t=0,
            costs=costs,
        )
        stack = [init_state]
        while len(stack) != 0:
            bp_geodes[bpi] = solver(stack.pop(0), stack, bp_geodes[bpi])
            pass
        # print(bpi, bp_geodes[bpi])
    answer = int(sum([np.product(x, dtype=int) for x in bp_geodes.items()]))
    print(bp_geodes, answer)
    return answer


main1(TEST_DATA_A)
print(TEST_RESULT_A)

# resa = main1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa
# %%

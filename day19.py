# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
import re

puz = Puzzle(year=2022, day=19)
print(puz.url)

# %%
# puz.input_data
# %%
TEST_DATA_A = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.\nBlueprint 2:Each ore robot costs 2 ore.Each clay robot costs 3 ore.Each obsidian robot costs 3 ore and 8 clay.Each geode robot costs 3 ore and 12 obsidian."
TEST_RESULT_A = 33
TEST_DATA_B = None
TEST_RESULT_B = None


def format_data(data):
    info = {}
    for line in data.split("\n"):
        bp, orob, crob, orobo, orobc, grobo, grobb = re.findall(r"\d+", line)
        info[bp] = {
            "orob_o": orob,
            "crob_o": crob,
            "obrob_o": orobo,
            "obrob_c": orobc,
            "grob_o": grobo,
            "grob_ob": grobb,
        }
    return info


def main1(data=None):
    pass


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

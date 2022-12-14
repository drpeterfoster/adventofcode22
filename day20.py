# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from tqdm import tqdm

puz = Puzzle(year=2022, day=20)
print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "1\n2\n-3\n3\n-2\n0\n4"
TEST_RESULT_A = 3
TEST_DATA_B = None
TEST_RESULT_B = 1623178306


def format_data(data):
    """start id, value, current index"""
    return {i: [int(x), i] for i, x in enumerate(data.split("\n"))}


def resort(vals):
    return list(zip(*list(sorted(list(vals.values()), key=lambda x: x[1]))))


def demixer(vals):
    n = len(vals)
    for i in tqdm(range(len(vals))):
        val, curr = vals[i]
        newraw = curr + val
        newmod = newraw % (n - 1) if (newraw >= n or newraw < 0) else newraw % n
        if val == 0:
            pass
        elif curr < newmod:
            modrange = list(range(curr + 1, newmod + 1))
            for k, v in vals.items():
                if v[1] in modrange:
                    vals[k][1] -= 1
            vals[i][1] = newmod
        elif newmod < curr:
            modrange = list(range(newmod, curr))
            for k, v in vals.items():
                if v[1] in modrange:
                    vals[k][1] += 1
            vals[i][1] = newmod
        else:
            ValueError("oops")
        # print(resort(vals))
    return vals


def answerer(vals, xyz=[1000, 2000, 3000]):
    final, _ = resort(vals)
    n = len(final)
    offset = np.argwhere(np.array(final) == 0)[0, 0]
    answer = sum([final[(v + offset) % n] for v in xyz])
    return answer


def main1(data=None):
    vals = format_data(data)
    vals = demixer(vals)
    answer = answerer(vals)
    # print(answer)
    return answer


def main2(data=None):
    vals = format_data(data)
    vals = {k: [v * 811589153, i] for k, (v, i) in vals.items()}
    for _ in range(10):
        vals = demixer(vals)
    answer = answerer(vals)
    return answer


def test_main_1(seq="-1\n15\n0\n-8\n2\n5"):
    res = main1(seq)
    assert res == -3


def test_main_2(seq="1\n3\n0\n-8\n-15"):
    res = main1(seq)
    assert res == 0


test_main_1()
test_main_2()

assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%

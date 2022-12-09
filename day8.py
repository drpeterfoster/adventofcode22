# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=1)

# %%
# puz.input_data
# %%
TEST_DATA_A = None
TEST_RESULT_A = None
TEST_DATA_B = None
TEST_RESULT_B = None


def main1(data):
    arr = np.array([list(map(int,x)) for x in data.split('\n')])
    idx = []
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if i == 0 or j == 0 or i == arr.shape[0]-1 or j == arr.shape[1]-1:
                idx.append((i,j))
            elif (arr[i,j] > arr[:i,j].max()
                  or arr[i,j] > arr[i+1:,j].max()
                  or arr[i,j] > arr[i,:j].max()
                  or arr[i,j] > arr[i,j+1:].max()):
                idx.append((i,j))
            else:
                pass
    return idx


def main2(data):
    arr = np.array([list(map(int,x)) for x in data.split('\n')])
    def _scorer(arr):
        vals = []
        for i in range(arr.shape[0]):
            lu, rd = 0, 0
            #left/up
            for k in range(i-1, -1, -1):
                if arr[k] < arr[i]:
                    lu += 1
                else:
                    lu += 1
                    break
            #right/down
            for k in range(i+1, arr.shape[0]):
                if arr[k] < arr[i]:
                    rd += 1
                else:
                    rd += 1
                    break
            vals.append((i, lu, rd))
        return vals

    subscores = {}
    for i in range(arr.shape[0]):
        _scores = _scorer(arr[i,:])
        for j, lu, rd in _scores:
            subscores[(i,j)] = [lu, rd]

    for j in range(arr.shape[1]):
        _scores = _scorer(arr[:,j])
        for i, lu, rd in _scores:
            subscores[(i,j)] += [lu, rd]

    scores = [np.product(x) for x in subscores.values()]
    return max(scores)


idx = main1(puz.input_data)
resa = len(set(idx))
print(f'solution: {resa}')
# puz.answer_a = resa

resb = main2(puz.input_data)
print(f'solution: {resb}')
# puz.answer_b = resb
# %%

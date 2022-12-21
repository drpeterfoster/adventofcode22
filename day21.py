# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from sympy import symbols, nsolve


puz = Puzzle(year=2022, day=21)
print(puz.url)

# %%
# puz.input_data
# %%
TEST_DATA_A = "root: pppw + sjmn\ndbpl: 5\ncczh: sllz + lgvd\nzczc: 2\nptdq: humn - dvpt\ndvpt: 3\nlfqf: 4\nhumn: 5\nljgn: 2\nsjmn: drzm * dbpl\nsllz: 4\npppw: cczh / lfqf\nlgvd: ljgn * ptdq\ndrzm: hmdt - zczc\nhmdt: 32"
TEST_RESULT_A = 152
TEST_DATA_B = None
TEST_RESULT_B = 301


def main1(data=None):
    info = [line.replace(": ", " = ") for line in data.split("\n")]
    while len(info) > 0:
        try:
            exec(info[0])
            info.pop(0)
        except NameError:
            tmp = info.pop(0)
            info.append(tmp)
    return locals()["root"]


def main2(data=None):
    info = [line.replace(": ", " = ") for line in data.split("\n")]
    for i, op in enumerate(info):
        if op.startswith("root = "):
            _op = op.split()
            funcstr = op.replace(_op[-2], "-")[7:]
            info.remove(op)
        elif op.startswith("humn ="):
            info[i] = " ".join(op.split()[:-1] + ["x"])
        else:
            continue
    while len(info) > 0:
        ops = info[0].split()
        if ops[0] in funcstr:
            funcstr = funcstr.replace(ops[0], f"({' '.join(ops[2:])})")
            info.pop(0)
        else:
            tmp = info.pop(0)
            info.append(tmp)
    x = symbols("x")
    answer = int(nsolve(eval(funcstr), 0))
    return answer


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%

# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from sympy import nsolve, Symbol

puz = Puzzle(year=2022, day=25)
print(puz.url)

# puz.input_data
# %%
TEST_DATA_A = "1=-0-2\n12111\n2=0=\n21\n2=01\n111\n20012\n112\n1=-1=\n1-12\n12\n1=\n122"
TEST_DATA_A_DEC = [1747, 906, 198, 11, 201, 31, 1257, 32, 353, 107, 7, 3, 37]
TEST_RESULT_A = "2=-1=0"
TEST_RESULT_A_DEC = 4890
TEST_DEC2SNAFU = {
    1: "1",
    2: "2",
    3: "1=",
    4: "1-",
    5: "10",
    6: "11",
    7: "12",
    8: "2=",
    9: "2-",
    10: "20",
    15: "1=0",
    20: "1-0",
    2022: "1=11-2",
    12345: "1-0---0",
    314159265: "1121-1110-1=0",
}
TEST_DATA_B = None
TEST_RESULT_B = None


SNAFU_2_INT = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
INT_2_SNAFU = {v: k for k, v in SNAFU_2_INT.items()}
SNAFU_MULTS = {i: 5**i for i in range(21)}


def format_data(data):
    snafus = [[SNAFU_2_INT[el] for el in line] for line in data.split("\n")]
    return snafus


def dec2snafu(dec):
    vals = []
    for i in range(20, -1, -1):
        val = round(dec / SNAFU_MULTS[i])
        dec = dec - SNAFU_MULTS[i] * val
        vals.append(val)
    snafu = "".join([INT_2_SNAFU[val] for val in vals])
    snafu = snafu.lstrip("0")
    return snafu


def test_dec2snafu(decdict=TEST_DEC2SNAFU):
    for dec, snafu in decdict.items():
        res = dec2snafu(dec)
        assert res == snafu


test_dec2snafu()


def main1(data=None):
    snafus = format_data(data)
    total_decs = [
        sum([SNAFU_MULTS[i] * val for i, val in enumerate(record[::-1])])
        for record in snafus
    ]
    sum_dec = sum(total_decs)
    sum_snafu = dec2snafu(sum_dec)
    return sum_snafu, sum_dec


def main2(data=None):
    pass


test_res_snafu, test_res_dec = main1(TEST_DATA_A)
assert test_res_snafu == TEST_RESULT_A
assert test_res_dec == TEST_RESULT_A_DEC
resa, _ = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

# assert main2(TEST_DATA_B) == TEST_RESULT_B
# resb = main2(puz.input_data)
# print(f'solution: {resb}')
# puz.answer_b = resb
# %%

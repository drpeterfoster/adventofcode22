# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=13)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "[1,1,3,1,1]\n[1,1,5,1,1]\n\n[[1],[2,3,4]]\n[[1],4]\n\n[9]\n[[8,7,6]]\n\n[[4,4],4,4]\n[[4,4],4,4,4]\n\n[7,7,7,7]\n[7,7,7]\n\n[]\n[3]\n\n[[[]]]\n[[]]\n\n[1,[2,[3,[4,[5,6,7]]]],8,9]\n[1,[2,[3,[4,[5,6,0]]]],8,9]"
TEST_RESULT_A = 13
TEST_DATA_B = None
TEST_RESULT_B = 140


def compare_int(a, b):
    if a < b:
        return True
    elif a == b:
        return None
    else:
        return False


def compare_list(a, b):
    checklist = []
    for x, y in zip(a, b):
        check = comparitor(x, y)
        checklist.append(check)
    for check in checklist:
        if check:
            return True
        elif check is None:
            pass
        else:
            return False
    # if the element-wise check doesn't have an opinion, defer to the length
    if len(a) < len(b):
        return True
    elif len(a) == len(b):
        return None
    else:
        return False


def comparitor(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return compare_int(a, b)
    elif isinstance(a, int) and isinstance(b, list):
        return compare_list([a], b)
    elif isinstance(a, list) and isinstance(b, int):
        return compare_list(a, [b])
    else:
        return compare_list(a, b)


def main1(data=None):
    right, wrong = [], []
    for i, packet in enumerate(data.split("\n\n")):
        a, b = list(map(eval, packet.split("\n")))
        check = comparitor(a, b)
        if check:
            right.append(i + 1)
        else:
            wrong.append(i + 1)
    return sum(right)


def main2(data=None):
    decoder_a, decoder_b = [[2]], [[6]]
    packets = [decoder_a, decoder_b]
    for packet in data.split("\n\n"):
        packets.extend(list(map(eval, packet.split("\n"))))
    done = False
    while not done:
        ordered = []
        for i in range(0, len(packets) - 1):
            check = comparitor(packets[i], packets[i + 1])
            ordered.append(check)
            if not check:
                packets[i], packets[i + 1] = packets[i + 1], packets[i]
        if all(ordered):
            done = True
    return eval(
        "*".join(
            [
                str(i + 1)
                for i, p in enumerate(packets)
                if p == decoder_a or p == decoder_b
            ]
        )
    )


assert main1(TEST_DATA_A) == TEST_RESULT_A
resa = main1(puz.input_data)
print(f"solution: {resa}")
puz.answer_a = resa

assert main2(TEST_DATA_A) == TEST_RESULT_B
resb = main2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%

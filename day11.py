# %%
import numpy as np
import pandas as pd
from aocd.models import Puzzle
from dataclasses import dataclass
from typing import List
from sympy.ntheory import factorint

puz = Puzzle(year=2022, day=11)
print(puz.url)

# %%
puz.input_data
# %%
TEST_DATA_A = "Monkey 0:\n  Starting items: 79, 98\n  Operation: new = old * 19\n  Test: divisible by 23\n    If true: throw to monkey 2\n    If false: throw to monkey 3\n\nMonkey 1:\n  Starting items: 54, 65, 75, 74\n  Operation: new = old + 6\n  Test: divisible by 19\n    If true: throw to monkey 2\n    If false: throw to monkey 0\n\nMonkey 2:\n  Starting items: 79, 60, 97\n  Operation: new = old * old\n  Test: divisible by 13\n    If true: throw to monkey 1\n    If false: throw to monkey 3\n\nMonkey 3:\n  Starting items: 74\n  Operation: new = old + 3\n  Test: divisible by 17\n    If true: throw to monkey 0\n    If false: throw to monkey 1"
TEST_RESULT_A = 10605
TEST_DATA_B = None
TEST_RESULT_B = 2713310158


##########  PART 1  ##########
@dataclass
class Monkey:
    id: int
    items: List[int]
    funcstr: str
    tval: int
    case_true: int
    case_false: int
    inspected: int = 0

    def func(self, old, stressed):
        val = eval(self.funcstr)
        if stressed:
            return val
        else:
            return val // 3


def parse_monkeys(data):
    monkeys = []
    for monkey in data.split("\n\n"):
        monkint = int(monkey.split()[-1])
        for line in monkey.split("\n"):
            match line.strip().split(": "):
                case ["Starting items", vals]:
                    items = list(map(int, vals.split(", ")))
                case ["Operation", op]:
                    funcstr = op.split(" = ")[-1]
                case ["Test", t]:
                    tval = int(t.split("divisible by ")[-1])
                case ["If true", val]:
                    ct = int(val.split()[-1])
                case ["If false", val]:
                    cf = int(val.split()[-1])
        monkey = Monkey(
            id=monkint,
            items=items,
            funcstr=funcstr,
            tval=tval,
            case_true=ct,
            case_false=cf,
        )
        monkeys.append(monkey)
    return monkeys


def main(data, rounds, stressed):
    monkeys = parse_monkeys(data)
    xanax = int(np.product([m.tval for m in monkeys]))
    for r in range(rounds):
        for m in monkeys:
            for i in range(len(m.items)):
                item = m.items.pop(0)
                item = m.func(item, stressed)
                if stressed:
                    item %= xanax
                if item % m.tval == 0:
                    monkeys[m.case_true].items.append(item)
                else:
                    monkeys[m.case_false].items.append(item)
                m.inspected += 1
    return int(np.product(list(sorted([m.inspected for m in monkeys]))[-2:]))


assert main(TEST_DATA_A, 20, False) == TEST_RESULT_A
resa = main(puz.input_data, 20, False)
print(f"solution: {resa}")
puz.answer_a = resa

assert main(TEST_DATA_A, 10_000, True) == TEST_RESULT_B
resb = main(puz.input_data, 10_000, True)
print(f"solution: {resb}")
puz.answer_b = resb

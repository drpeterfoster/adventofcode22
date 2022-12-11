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
    funcstr: str
    tval: int
    case_true: int
    case_false: int
    items: List[int] = None
    prime_items: List[List[int]] = None
    inspected: int = 0

    def func(self, old):
        val = eval(self.funcstr)
        return val // 3

    def primefunc(self, primes):
        if self.funcstr == "old * old":
            primes.extend(primes)
        elif self.funcstr.startswith("old *"):
            primes.append(int(self.funcstr.split()[-1]))
        elif self.funcstr.startswith("old +"):
            adder = int(self.funcstr.split()[-1])
            try:
                newval = int(np.product(primes)) + adder
                if newval < 0:
                    raise FloatingPointError(newval)
            except FloatingPointError:
                newval = eval("*".join(map(str, primes))) + adder
            primes = factor_primes(newval)
        else:
            raise ValueError("oops")
        return primes


def parse_monkeys(data):
    monkeys = []
    for monkey in data.split("\n\n"):
        monkint = int(monkey.split()[-1])
        for line in monkey.split("\n"):
            match line.strip().split(": "):
                case ["Starting items", vals]:
                    items = list(map(int, vals.split(", ")))
                    prime_items = list(
                        map(lambda x: factor_primes(int(x)), vals.split(", "))
                    )
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
            prime_items=prime_items,
            funcstr=funcstr,
            tval=tval,
            case_true=ct,
            case_false=cf,
        )
        monkeys.append(monkey)
    return monkeys


def main1(data, rounds):
    monkeys = parse_monkeys(data)
    for r in range(rounds):
        for m in monkeys:
            for i in range(len(m.items)):
                item = m.items.pop(0)
                item = m.func(item)
                if item % m.tval == 0:
                    monkeys[m.case_true].items.append(item)
                else:
                    monkeys[m.case_false].items.append(item)
                m.inspected += 1
    print([m.inspected for m in monkeys])
    return int(np.product(list(sorted([m.inspected for m in monkeys]))[-2:]))


# main1(TEST_DATA_A, 1000)
assert main1(TEST_DATA_A, 20) == TEST_RESULT_A
resa = main1(puz.input_data, 20)
print(f"solution: {resa}")
# puz.answer_a = resa

# %%
##########  PART 2  ##########
# # this version is too slow.  go faster!
# def factor_primes(n):
#     result = []
#     # Print the number of two's that divide n
#     while n % 2 == 0:
#         result.append(2)
#         n = n // 2
#     # n must be odd at this point so a skip of 2 ( i = i + 2) can be used
#     # for i in range(3, int(n**0.5) + 1, 2):
#         # while i divides n , print i and divide n
#         while n % i == 0:
#             result.append(i)
#             n = n // i
#     # Condition if n is a prime number greater than 2
#     if n > 2:
#         result.append(int(n))
#     return result


def factor_primes(n):
    return [k for k, v in factorint(n).items() for _ in range(v)]


def main2(data, rounds):
    monkeys = parse_monkeys(data)
    for r in range(rounds):
        for m in monkeys:
            for i in range(len(m.prime_items)):
                pi = m.prime_items.pop(0)
                pi = m.primefunc(pi)
                if m.tval in pi:
                    monkeys[m.case_true].prime_items.append(pi)
                else:
                    monkeys[m.case_false].prime_items.append(pi)
                m.inspected += 1
        if r % 100 == 0:
            print(r, end=" ")
    # print([m.inspected for m in monkeys])
    return int(np.product(list(sorted([m.inspected for m in monkeys]))[-2:]))


# Ok, so— this is still way too slow.  the numbers just get too big, too fast.
# I think the prime factorization idea is nice, but there's no shortcut for addition.
# I kinda wonder if there's a way to use the Part1 approach, just tracking the number
# of times the values are divided by 3 and the remainders... but I'm too annoyed
# to figure it out right now.  Maybe another time.

# testb = main2(TEST_DATA_A, 1000)
# assert testb == TEST_RESULT_B
# resb = main2(puz.input_data, 10_000)
# print(f"solution: {resb}")
# puz.answer_b = resb
# %%
# # tester code— don't really care to refactor the above.
# def main(data, rounds):
#     monkeys = parse_monkeys(data)
#     for r in range(rounds):
#         for m in monkeys:
#             for i in range(len(m.items)):
#                 item = m.items.pop(0)
#                 item = m.func(item)
#                 pi = m.prime_items.pop(0)
#                 pi = m.primefunc(pi)
#                 item_test = item % m.tval == 0
#                 if item_test:
#                     monkeys[m.case_true].items.append(item)
#                 else:
#                     monkeys[m.case_false].items.append(item)
#                 pi_test = m.tval in pi
#                 if pi_test:
#                     monkeys[m.case_true].prime_items.append(pi)
#                 else:
#                     monkeys[m.case_false].prime_items.append(pi)
#                 m.inspected += 1
#                 if item_test != pi_test:
#                     raise ValueError(
#                         f"r: {r} shows {item_test} vs {pi_test} using {m.tval}\n{item} ||| {pi}"
#                     )
#     print([m.inspected for m in monkeys])
#     return int(np.product(list(sorted([m.inspected for m in monkeys]))[-2:]))


# main(TEST_DATA_A, 1000)
# %%

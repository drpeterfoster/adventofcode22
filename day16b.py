# %%
from aocd.models import Puzzle

puz = Puzzle(year=2022, day=16)
print(puz.url)


import itertools
from tqdm import tqdm


def parse(lines):
    for line in lines.split("\n"):
        tokens = line.split(" ")
        yield tokens[1], int(tokens[4].split("=")[1].strip(";")), [
            x.strip(",\n") for x in tokens[9:]
        ]


def find_shortest_path(A, B, tunnels):
    def walk(node, path, visited):
        new_visited = {*visited, node}
        if B in tunnels[node]:
            return path + [B]
        else:
            paths = [
                x
                for x in [
                    walk(N, path + [N], new_visited)
                    for N in set(tunnels[node]) - visited
                ]
                if x
            ]
            if paths:
                min_len = min(len(x) for x in paths)
                return next(x for x in paths if len(x) == min_len)
            else:
                return None

    return walk(A, [], set())


def solution1(lines):
    flow_rates = {}
    tunnels = {}

    for valve, flow_rate, neighbors in parse(lines):
        flow_rates[valve] = flow_rate
        tunnels[valve] = neighbors

    shortest_paths = {}
    for A, B in itertools.product(
        tunnels.keys(), [t for t in tunnels.keys() if flow_rates[t] > 0]
    ):
        path = find_shortest_path(A, B, tunnels)
        if path:
            shortest_paths[(A, B)] = path

    # print(shortest_paths)

    all_valves = set(x for x in flow_rates.keys() if flow_rates[x] > 0)

    def walk(valve, open_valves, total_pressure, minute):
        this_minute_pressure = sum(flow_rates[v] for v in open_valves)

        if minute > 29:
            return total_pressure

        pressures = []
        if valve not in open_valves and flow_rates[valve] > 0:
            return walk(
                valve,
                {*open_valves, valve},
                total_pressure + this_minute_pressure,
                minute + 1,
            )

        remaining_valves = all_valves - open_valves
        next_paths = list(
            shortest_paths[valve, x]
            for x in remaining_valves
            if (valve, x) in shortest_paths and x not in open_valves
        )
        for t in next_paths:
            if minute + len(t) < 30:
                pressures.append(
                    walk(
                        t[-1],
                        open_valves,
                        total_pressure + (this_minute_pressure * len(t)),
                        minute + len(t),
                    )
                )

        return (
            max(pressures)
            if len(pressures)
            else walk(
                valve, open_valves, total_pressure + this_minute_pressure, minute + 1
            )
        )

    return walk("AA", set(), 0, 0)


def solution2(lines):
    flow_rates = {}
    tunnels = {}

    for valve, flow_rate, neighbors in parse(lines):
        flow_rates[valve] = flow_rate
        tunnels[valve] = neighbors

    shortest_paths = {}
    for A, B in itertools.product(
        tunnels.keys(), [t for t in tunnels.keys() if flow_rates[t] > 0]
    ):
        path = find_shortest_path(A, B, tunnels)
        if path:
            shortest_paths[(A, B)] = path

    # print(shortest_paths)

    def walk(valve, open_valves, total_pressure, minute, all_valves):
        this_minute_pressure = sum(flow_rates[v] for v in open_valves)

        if minute > 25:
            return total_pressure

        pressures = []
        if valve not in open_valves and flow_rates[valve] > 0:
            return walk(
                valve,
                {*open_valves, valve},
                total_pressure + this_minute_pressure,
                minute + 1,
                all_valves,
            )

        remaining_valves = all_valves - open_valves
        next_paths = list(
            shortest_paths[valve, x]
            for x in remaining_valves
            if (valve, x) in shortest_paths and x not in open_valves
        )
        for t in next_paths:
            if minute + len(t) < 26:
                pressures.append(
                    walk(
                        t[-1],
                        open_valves,
                        total_pressure + (this_minute_pressure * len(t)),
                        minute + len(t),
                        all_valves,
                    )
                )

        return (
            max(pressures)
            if len(pressures)
            else walk(
                valve,
                open_valves,
                total_pressure + this_minute_pressure,
                minute + 1,
                all_valves,
            )
        )

    max_total = 0
    target_valves = set(x for x in flow_rates.keys() if flow_rates[x] > 0)
    for combs in tqdm(
        [
            combs
            for r in range(len(target_valves) // 2)
            for combs in tqdm(itertools.combinations(target_valves, r))
        ]
    ):
        total = walk("AA", set(), 0, 0, set(combs)) + walk(
            "AA", set(), 0, 0, target_valves - set(combs)
        )
        max_total = max(total, max_total)
    return max_total


# resa = solution1(puz.input_data)
# print(f"solution: {resa}")
# puz.answer_a = resa

resb = solution2(puz.input_data)
print(f"solution: {resb}")
puz.answer_b = resb
# %%

#! /usr/bin/python3.12
import csv
from collections import defaultdict
from typing import List, Tuple

NUMPAD = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}

ARROWPAD = {
    "A": (0, 2),
    "^": (0, 1),
    ">": (1, 2),
    "v": (1, 1),
    "<": (1, 0),
}

TOTAL_LAYERS = 3


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.code_lens = {}

    def populate_code_lens(self):
        cache = defaultdict(int)

        def get_partial_strs(
            s_r: int, s_c: int, diff_r: int, diff_c: int, layer: int
        ) -> List[str]:
            """Returns possible paths from (s_r, s_c) given input diffs/layer.

            Will only return paths that do not pass through an empty space in
            either NUMPAD or ARROWPAD depending on the layer that is calling
            this function.
            """
            # [r_first_str, c_first_str]
            partial_strs = ["", ""]

            valid_r_first_str = (
                layer == 0 and (s_r + diff_r, s_c) in NUMPAD.values()
            ) or (layer > 0 and (s_r + diff_r, s_c) in ARROWPAD.values())
            valid_c_first_str = (
                layer == 0 and (s_r, s_c + diff_c) in NUMPAD.values()
            ) or (layer > 0 and (s_r, s_c + diff_c) in ARROWPAD.values())

            if valid_r_first_str:
                for _ in range(abs(diff_r)):
                    if diff_r < 0:
                        partial_strs[0] += "^"
                    elif diff_r > 0:
                        partial_strs[0] += "v"

                for _ in range(abs(diff_c)):
                    if diff_c < 0:
                        partial_strs[0] += "<"
                    elif diff_c > 0:
                        partial_strs[0] += ">"

            if valid_c_first_str:
                for _ in range(abs(diff_c)):
                    if diff_c < 0:
                        partial_strs[1] += "<"
                    elif diff_c > 0:
                        partial_strs[1] += ">"

                for _ in range(abs(diff_r)):
                    if diff_r < 0:
                        partial_strs[1] += "^"
                    elif diff_r > 0:
                        partial_strs[1] += "v"

            return [partial_str for partial_str in partial_strs if partial_str != ""]

        def get_num_moves(src: str, dst: str, layer: int) -> int:
            """Finds number of moves from src to dst on current layer.

            Will recursively call itself up to TOTAL_LAYERS, and cache
            intermediate results per layer. Call hierarchy is essentially DFS
            chunked by each "A" press, as each layer will return to "A" as
            part of the input path for the previous layer.
            """
            if (src, dst, layer) in cache:
                return cache[(src, dst, layer)]

            s_r, s_c = NUMPAD[src] if layer == 0 else ARROWPAD[src]
            d_r, d_c = NUMPAD[dst] if layer == 0 else ARROWPAD[dst]

            diff_r, diff_c = d_r - s_r, d_c - s_c

            # Last layer just needs to reach dst and click "A"
            if layer == TOTAL_LAYERS - 1:
                return abs(diff_r) + abs(diff_c) + 1

            shortest_strs = []

            partial_strs = get_partial_strs(s_r, s_c, diff_r, diff_c, layer)

            # Recursively compute length for next layer
            for partial_str in set(partial_strs):
                next_layer_src = "A"
                moves = 0

                for c in partial_str:
                    moves += get_num_moves(next_layer_src, c, layer + 1)
                    next_layer_src = c
                
                # Always finish at "A"
                moves += get_num_moves(next_layer_src, "A", layer + 1)
                shortest_strs.append(moves)

            # src == dst, so just press A one time
            if not partial_strs:
                return 1

            cache[(src, dst, layer)] = min(shortest_strs)
            return min(shortest_strs)

        def populate_code_len(code: str):
            total_len = get_num_moves("A", code[0], 0)

            for idx in range(len(code) - 1):
                total_len += get_num_moves(code[idx], code[idx + 1], 0)

            self.code_lens[code] = total_len

        for code in self.code_lens:
            populate_code_len(code)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            complexity = 0

            for row in csv_reader:
                self.code_lens[row[0]] = -1

            self.populate_code_lens()

            for code in self.code_lens:
                complexity += self.code_lens[code] * int(code[:-1])

            print(complexity)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv
from collections import defaultdict
from typing import Set, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.rows = 0
        self.cols = 0

    def get_valid_antinodes(
        self, node: Tuple[int, int], pair: Tuple[int, int]
    ) -> Set[Tuple[int, int]]:
        """Returns the valid unique antinodes for the given node pair.

        Will keep a running multiplier starting at 0 to account for all
        resonant harmonics, and stop when exceeding map boundaries.
        """

        def is_valid(r: int, c: int) -> bool:
            return 0 <= r < self.rows and 0 <= c < self.cols

        d_np_r, d_np_c = pair[0] - node[0], pair[1] - node[1]
        valid_antinodes = set()
        plus_mult = 0
        minus_mult = 0

        while is_valid(pair[0] + (plus_mult * d_np_r), pair[1] + (plus_mult * d_np_c)):
            valid_antinodes.add(
                (pair[0] + (plus_mult * d_np_r), pair[1] + (plus_mult * d_np_c))
            )
            plus_mult += 1

        while is_valid(
            node[0] - (minus_mult * d_np_r), node[1] - (minus_mult * d_np_c)
        ):
            valid_antinodes.add(
                (node[0] - (minus_mult * d_np_r), node[1] - (minus_mult * d_np_c))
            )
            minus_mult += 1

        return valid_antinodes

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            valid_antinodes = set()
            node_locations = defaultdict(list)
            curr_row = 0

            for row in csv_reader:
                for idx, c in enumerate(row[0]):
                    if c != ".":
                        node_locations[c].append((curr_row, idx))
                self.cols = len(row[0])
                curr_row += 1

            self.rows = curr_row

            for freq in node_locations:
                nodes = node_locations[freq]
                if len(nodes) > 1:
                    for node_idx in range(len(nodes) - 1):
                        for pair_idx in range(node_idx + 1, len(nodes)):
                            valid_antinodes.update(
                                self.get_valid_antinodes(
                                    nodes[node_idx], nodes[pair_idx]
                                )
                            )

            print(len(valid_antinodes))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

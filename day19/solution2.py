#! /usr/bin/python3.12
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.trie = {}

    def add_towel_to_trie(self, towel: str):
        curr = self.trie

        for c in towel:
            if c not in curr:
                curr[c] = {}
            curr = curr[c]

        # Termination char
        curr["."] = True

    def valid_arrangements(self, design: str) -> bool:
        """Counts # of ways the input design is buildable with given towels.

        Caches results of helper function that counts the number of ways that
        the end can be reached using valid towel sequences, at each starting
        index of the given design.
        """
        cache = [None for _ in range(len(design))]

        def num_ways_reach_end(start_idx: int) -> int:
            if start_idx == len(design):
                return 1
            elif cache[start_idx] is not None:
                return cache[start_idx]

            curr = self.trie
            d_idx = start_idx
            num_ways = 0

            while d_idx < len(design) and design[d_idx] in curr:
                curr = curr[design[d_idx]]

                # Can attempt recursive call
                if "." in curr:
                    num_ways += num_ways_reach_end(d_idx + 1)

                d_idx += 1

            cache[start_idx] = num_ways

            return num_ways

        return num_ways_reach_end(0)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            designs = []
            valid_arrangements = 0

            for row in csv_reader:
                if not row:
                    continue
                elif len(row) > 1:
                    for towel in row:
                        self.add_towel_to_trie(towel.strip())
                else:
                    designs.append(row[0])

            for design in designs:
                valid_arrangements += self.valid_arrangements(design)

            print(valid_arrangements)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

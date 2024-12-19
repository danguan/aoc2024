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

    def is_valid_design(self, design: str) -> bool:
        """Identifies whether the input design is buildable with given towels.

        Caches results of helper function that determines whether the entire
        design is buildable from given index, assuming that each recursive call
        will only occur after a full towel sequence.
        """
        cache = [None for _ in range(len(design))]

        def can_reach_end(start_idx: int) -> bool:
            if start_idx == len(design):
                return True
            elif cache[start_idx] is False:
                return False

            curr = self.trie
            d_idx = start_idx

            while d_idx < len(design) and design[d_idx] in curr:
                curr = curr[design[d_idx]]

                # Can attempt recursive call
                if "." in curr:
                    if can_reach_end(d_idx + 1):
                        return True

                d_idx += 1                

            cache[start_idx] = False

            return False

        return can_reach_end(0)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            designs = []
            valid_designs = 0

            for row in csv_reader:
                if not row:
                    continue
                elif len(row) > 1:
                    for towel in row:
                        self.add_towel_to_trie(towel.strip())
                else:
                    designs.append(row[0])

            for design in designs:
                if self.is_valid_design(design):
                    valid_designs += 1

            print(valid_designs)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

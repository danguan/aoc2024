#! /usr/bin/python3.12
import csv
from collections import defaultdict

BLINKS = 75
NO_RULE_MULT = 2024


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.cache = defaultdict(dict)

    def stone_count_after_blinks(self, stone: int, blinks: int) -> int:
        """Returns number of stones for current stone after input # of blinks."""
        stone_len = len(str(stone))
        if blinks in self.cache[stone]:
            return self.cache[stone][blinks]

        if blinks == 0:
            return 1
        elif stone == 0:
            self.cache[stone][blinks] = self.stone_count_after_blinks(1, blinks - 1)
        elif stone_len % 2 == 0:
            self.cache[stone][blinks] = self.stone_count_after_blinks(
                int(str(stone)[: stone_len // 2]), blinks - 1
            ) + self.stone_count_after_blinks(
                int(str(stone)[stone_len // 2 :]), blinks - 1
            )
        else:
            self.cache[stone][blinks] = self.stone_count_after_blinks(
                stone * NO_RULE_MULT, blinks - 1
            )

        return self.cache[stone][blinks]

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            stones = []
            total_stones = 0

            for row in csv_reader:
                stones = [int(num) for num in row[0].split(" ")]

            for stone in stones:
                total_stones += self.stone_count_after_blinks(stone, BLINKS)

            print(total_stones)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

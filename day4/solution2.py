#! /usr/bin/python3.12
import csv

DIRS = [(-1, -1), (-1, 1), (1, 1), (1, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def is_xmas(self, r: int, c: int) -> bool:
        """Returns whether r,c is the center of an X-MAS formation.

        Assumption: Initial r,c spot is "A" character, to reduce amount of
        calls to process.
        """
        rotation_string = ""

        if r == 0 or r == len(self.grid) - 1 or c == 0 or c == len(self.grid[0]) - 1:
            return False

        for d_r, d_c in DIRS:
            rotation_string += self.grid[r + d_r][c + d_c]

        return "MMSS" in (rotation_string + rotation_string)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_xmas = 0

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for r in range(len(self.grid)):
                for c in range(len(self.grid[0])):
                    if self.grid[r][c] == "A":
                        total_xmas += 1 if self.is_xmas(r, c) else 0

            print(total_xmas)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

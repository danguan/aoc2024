#! /usr/bin/python3.12
import csv

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def count_xmas(self, r: int, c: int) -> int:
        """Returns # of times XMAS appears in each direction from input r,c.

        Will pre-emptively check each direction for length available to
        continue looking for remainder of XMAS string, before checking the
        characters themselves.

        Assumption: Initial r,c spot is "X" character, to reduce amount of
        calls to process.
        """
        subtotal_xmas = 0
        target = "XMAS"

        def check_xmas_directional(
            curr_r: int, curr_c: int, d_r: int, d_c: int, target_idx: int
        ) -> bool:
            if self.grid[curr_r][curr_c] == target[target_idx]:
                if target_idx == len(target) - 1:
                    return True
                return check_xmas_directional(
                    curr_r + d_r, curr_c + d_c, d_r, d_c, target_idx + 1
                )

            return False

        for d_r, d_c in DIRS:
            if 0 <= r + (d_r * (len(target) - 1)) < len(self.grid) and 0 <= c + (
                d_c * (len(target) - 1)
            ) < len(self.grid[0]):
                subtotal_xmas += (
                    1 if check_xmas_directional(r + d_r, c + d_c, d_r, d_c, 1) else 0
                )

        return subtotal_xmas

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_xmas = 0

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for r in range(len(self.grid)):
                for c in range(len(self.grid[0])):
                    if self.grid[r][c] == "X":
                        total_xmas += self.count_xmas(r, c)

            print(total_xmas)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

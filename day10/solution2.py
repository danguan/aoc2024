#! /usr/bin/python3.12
import csv
from collections import deque

DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
MAX_HEIGHT = 9


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def get_trailhead_rating(self, r: int, c: int) -> int:
        """Calculates rating of trailhead at given r,c using BFS."""

        total_ends = 0
        q = deque([(r, c, 0)])

        while q:
            curr_r, curr_c, height = q.popleft()

            for d_r, d_c in DIRS:
                new_r, new_c = curr_r + d_r, curr_c + d_c

                if (
                    0 <= new_r < len(self.grid)
                    and 0 <= new_c < len(self.grid[0])
                    and self.grid[new_r][new_c] == height + 1
                ):
                    if height + 1 == MAX_HEIGHT:
                        total_ends += 1
                    else:
                        q.append((new_r, new_c, height + 1))
        return total_ends

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            trailheads = []
            trailhead_sum = 0
            curr_row = 0

            for row in csv_reader:
                row_to_add = []
                for idx, c in enumerate(row[0]):
                    if c == "0":
                        trailheads.append((curr_row, idx))
                    row_to_add.append(int(c))
                self.grid.append(row_to_add)
                curr_row += 1

            for r, c in trailheads:
                trailhead_sum += self.get_trailhead_rating(r, c)

            print(trailhead_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv
from collections import deque
from typing import Tuple

GRID_SIZE = 71
FALL_SIZE = 1024
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def bfs(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        """Use BFS to find shortest path from input start to input end."""
        seen = set([start])
        q = deque([(start, 0)])

        while q:
            (r, c), score = q.popleft()

            for d_r, d_c in DIRS:
                new_r, new_c = r + d_r, c + d_c

                if (
                    0 <= new_r < GRID_SIZE
                    and 0 <= new_c < GRID_SIZE
                    and (new_r, new_c) not in seen
                    and self.grid[new_r][new_c] == "."
                ):
                    if (new_r, new_c) == end:
                        return score + 1
                    seen.add((new_r, new_c))
                    q.append(((new_r, new_c), score + 1))

        return -1

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for r_idx, row in enumerate(csv_reader):
                if r_idx >= FALL_SIZE:
                    break

                self.grid[int(row[1])][int(row[0])] = "#"

            print(self.bfs((0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

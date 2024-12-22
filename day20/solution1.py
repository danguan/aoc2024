#! /usr/bin/python3.12
import csv
from collections import deque
from typing import Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []
        self.inner_walls = []

    def get_solve_time(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        q = deque([(start, 0)])
        seen = set([start])

        while q:
            (r, c), time = q.popleft()

            for d_r, d_c in DIRS:
                new_r, new_c = r + d_r, c + d_c

                if (
                    0 <= new_r < len(self.grid)
                    and 0 <= new_c < len(self.grid[0])
                    and (new_r, new_c) not in seen
                ):
                    if (new_r, new_c) == end:
                        return time
                    elif self.grid[new_r][new_c] == ".":
                        seen.add((new_r, new_c))
                        q.append(((new_r, new_c), time + 1))

        return -1

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            start = (-1, -1)
            end = (-1, -1)
            good_cheats = 0

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for r in range(1, len(self.grid) - 1):
                for c in range(1, len(self.grid[0]) - 1):
                    if self.grid[r][c] == "#":
                        self.inner_walls.append((r, c))
                    elif self.grid[r][c] == "S":
                        start = (r, c)
                    elif self.grid[r][c] == "E":
                        end = (r, c)

            no_obstacle_time = self.get_solve_time(start, end)

            for i_r, i_c in self.inner_walls:
                self.grid[i_r][i_c] = "."

                if self.get_solve_time(start, end) <= no_obstacle_time - 100:
                    good_cheats += 1

                self.grid[i_r][i_c] = "#"

            print(good_cheats)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

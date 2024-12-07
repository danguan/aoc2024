#! /usr/bin/python3.12
import csv

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def is_valid_position(self, r: int, c: int) -> bool:
        """Returns whether the given r,c is within grid bounds."""
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            curr = (-1, -1)
            direction_idx = 0
            visited = 1

            for row in csv_reader:
                new_row = []
                for idx, c in enumerate(row[0]):
                    if c == "^":
                        curr = (len(self.grid), idx)
                        new_row.append("X")
                    else:
                        new_row.append(c)

                self.grid.append(new_row)
            
            while True:
                d_r, d_c = DIRS[direction_idx]
                new_r, new_c = curr[0] + d_r, curr[1] + d_c

                if not self.is_valid_position(new_r, new_c):
                    break
                elif self.grid[new_r][new_c] == "#":
                    direction_idx = (direction_idx + 1) % len(DIRS)
                else:
                    if self.grid[new_r][new_c] == ".":
                        visited += 1
                        self.grid[new_r][new_c] = "X"
                    curr = (new_r, new_c)

            print(visited)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv
from typing import Tuple

DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []
        self.moves = []
        self.start = (-1, -1)

    def get_box_coords(self) -> int:
        """Finds the total value of all box GPS coordinates."""
        total_box_coords = 0

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == "O":
                    total_box_coords += (100 * r) + c

        return total_box_coords

    def do_moves(self):
        """Simulate all of `self.moves` in place on `self.grid`.

        Pushing boxes entails finding first empty space and switching box with
        empty space, then moving forwards.
        """
        r, c = self.start

        def first_empty_space(r: int, c: int, d_r: int, d_c: int) -> Tuple[int, int]:
            while self.grid[r][c] == "O":
                r += d_r
                c += d_c

            if self.grid[r][c] == ".":
                return (r, c)

            return (-1, -1)

        for move in self.moves:
            d_r, d_c = DIRS[move]
            new_r, new_c = r + d_r, c + d_c

            # Wall
            if self.grid[new_r][new_c] == "#":
                continue
            # Box
            elif self.grid[new_r][new_c] == "O":
                empty_space_r, empty_space_c = first_empty_space(new_r, new_c, d_r, d_c)
                if (empty_space_r, empty_space_c) == (-1, -1):
                    continue

                self.grid[empty_space_r][empty_space_c] = "O"
                self.grid[new_r][new_c] = "."

            # Empty space
            if self.grid[new_r][new_c] == ".":
                self.grid[r][c] = "."
                self.grid[new_r][new_c] = "@"
                r, c = new_r, new_c

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            grid = True

            for row_idx, row in enumerate(csv_reader):
                if not row:
                    grid = False
                elif row and grid:
                    grid_row = []
                    for idx, c in enumerate(row[0]):
                        grid_row.append(c)
                        if c == "@":
                            self.start = (row_idx, idx)
                    self.grid.append(grid_row)
                else:
                    self.moves.extend([c for c in row[0]])

            self.do_moves()
            print(self.get_box_coords())


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

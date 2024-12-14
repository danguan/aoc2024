#! /usr/bin/python3.12
import csv
from collections import deque
from typing import Tuple


DIRS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def in_bounds(self, r, c) -> bool:
        return 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0])

    def get_price(self, start_r: int, start_c: int, orig_value: str, id: int) -> int:
        """Calculates price for region starting at (start_r, start_c).

        Identify number of corners per region, which should be equal to the
        number of sides for the region, and can thus be multiplied with the
        area to get the full price.
        """
        seen = set([(start_r, start_c)])
        q = deque([(start_r, start_c)])
        total_area = 0
        total_corners = 0

        while q:
            r, c = q.popleft()
            self.grid[r][c] = id
            total_area += 1

            for idx, (d_r, d_c) in enumerate(DIRS):
                new_r, new_c = r + d_r, c + d_c

                if idx % 2 == 1:
                    corner_same = (
                        (self.grid[new_r][new_c] in [orig_value, id])
                        if self.in_bounds(new_r, new_c)
                        else True
                    )
                    # Looks like:
                    #   XX
                    #   XO
                    # where O is self.grid[r][c] and DIR is (-1, -1)
                    convex_corner = (
                        not self.in_bounds(new_r, c)
                        or self.grid[new_r][c] not in [orig_value, id]
                    ) and (
                        not self.in_bounds(r, new_c)
                        or self.grid[r][new_c] not in [orig_value, id]
                    )
                    # Looks like:
                    #   XO
                    #   OO
                    # where bottom right O is self.grid[r][c] and DIR is (-1, -1)
                    concave_corner = (
                        self.in_bounds(new_r, c)
                        and self.grid[new_r][c] in [orig_value, id]
                        and self.in_bounds(r, new_c)
                        and self.grid[r][new_c] in [orig_value, id]
                        and not corner_same
                    )

                    if convex_corner or concave_corner:
                        total_corners += 1
                elif self.in_bounds(new_r, new_c):
                    if (new_r, new_c) in seen:
                        continue
                    elif self.grid[new_r][new_c] == orig_value:
                        q.append((new_r, new_c))
                        seen.add((new_r, new_c))
        return total_area * total_corners

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            total_price = 0
            id = 0

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    if isinstance(self.grid[row][col], str):
                        orig_value = self.grid[row][col]
                        total_price += self.get_price(row, col, orig_value, id)
                        id += 1

            print(total_price)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

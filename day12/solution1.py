#! /usr/bin/python3.12
import csv
from collections import deque
from typing import Tuple


DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def get_price(self, start_r: int, start_c: int) -> int:
        """Calculates price for region starting at (start_r, start_c).

        Using BFS, accumulate count for area and remove 1 perimeter for any
        identical/processed plants.
        """
        seen = set([(start_r, start_c)])
        q = deque([(start_r, start_c)])
        total_area = 0
        total_perimeter = 0

        while q:
            r, c = q.popleft()
            self.grid[r][c] = self.grid[r][c].lower()
            total_area += 1
            curr_perim = 4

            for d_r, d_c in DIRS:
                new_r, new_c = r + d_r, c + d_c

                if 0 <= new_r < len(self.grid) and 0 <= new_c < len(self.grid[0]):
                    if (new_r, new_c) in seen:
                        curr_perim -= 1
                        continue
                    elif self.grid[new_r][new_c] == self.grid[r][c].upper():
                        curr_perim -= 1
                        q.append((new_r, new_c))
                        seen.add((new_r, new_c))

            total_perimeter += curr_perim

        return total_area * total_perimeter

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            total_price = 0

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    if self.grid[row][col].isupper():
                        total_price += self.get_price(row, col)

            print(total_price)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv
import re

WIDTH = 101
HEIGHT = 103
SECONDS = 100


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            robots = []

            for row in csv_reader:
                if not row:
                    continue
                elif match := re.search(
                    r"p=(\d+),(\d+) v=(-*\d+),(-*\d+)", ",".join(row)
                ):
                    robots.append(
                        [
                            [int(match.group(2)), int(match.group(1))],
                            [int(match.group(4)), int(match.group(3))],
                        ]
                    )

            curr = 79
            for seconds in range(10000):
                grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

                for idx, robot in enumerate(robots):
                    (r, c), (d_r, d_c) = robot

                    robots[idx][0] = [(r + d_r) % HEIGHT, (c + d_c) % WIDTH]
                    grid[r][c] = "x"
                
                if seconds == curr:
                    print("--------")
                    print(seconds)
                    print("--------")
                    for row in grid:
                        print("".join(row))
                    print("\n")
                    curr += WIDTH



if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

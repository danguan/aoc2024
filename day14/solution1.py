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
            quads = [0, 0, 0, 0]

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

            for _ in range(SECONDS):
                for idx, robot in enumerate(robots):
                    (r, c), (d_r, d_c) = robot

                    robots[idx][0] = [(r + d_r) % HEIGHT, (c + d_c) % WIDTH]

            for (r, c), (_, _) in robots:
                if r < HEIGHT // 2:
                    if c < WIDTH // 2:
                        quads[0] += 1
                    elif c > WIDTH // 2:
                        quads[1] += 1
                elif r > HEIGHT // 2:
                    if c < WIDTH // 2:
                        quads[2] += 1
                    elif c > WIDTH // 2:
                        quads[3] += 1

            print(quads[0] * quads[1] * quads[2] * quads[3])


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

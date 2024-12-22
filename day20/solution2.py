#! /usr/bin/python3.12
import csv
from collections import defaultdict, deque
from typing import DefaultDict, Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
THRESHOLD = 100
MAX_CHEAT_LEN = 20


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def get_manhattan_dist(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def get_dists_from_src(
        self, src: Tuple[int, int]
    ) -> DefaultDict[Tuple[int, int], int]:
        """Finds the distance of all path spaces from given src tile."""
        dists = defaultdict(int)
        q = deque([(src, 0)])
        seen = set([src])

        while q:
            (r, c), dist = q.popleft()
            dists[(r, c)] = dist

            for d_r, d_c in DIRS:
                new_r, new_c = r + d_r, c + d_c

                if (
                    0 < new_r < len(self.grid) - 1
                    and 0 < new_c < len(self.grid[0]) - 1
                    and (new_r, new_c) not in seen
                    and self.grid[new_r][new_c] in ["S", ".", "E"]
                ):
                    q.append(((new_r, new_c), dist + 1))
                    seen.add((new_r, new_c))

        return dists

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            start = (-1, -1)
            end = (-1, -1)

            for row in csv_reader:
                self.grid.append([c for c in row[0]])

            for r in range(1, len(self.grid) - 1):
                for c in range(1, len(self.grid[0]) - 1):
                    if self.grid[r][c] == "S":
                        start = (r, c)
                    elif self.grid[r][c] == "E":
                        end = (r, c)

            dists_from_start = self.get_dists_from_src(start)
            no_cheat_dist = dists_from_start[end]
            dists_from_end = self.get_dists_from_src(end)

            good_cheats = []

            for s_r, s_c in dists_from_start:
                dist_from_start = dists_from_start[(s_r, s_c)]

                for e_r, e_c in dists_from_end:
                    dist_from_end = dists_from_end[(e_r, e_c)]

                    cheat_len = self.get_manhattan_dist((s_r, s_c), (e_r, e_c))

                    if cheat_len <= MAX_CHEAT_LEN and (
                        dist_from_start + cheat_len + dist_from_end
                        <= no_cheat_dist - THRESHOLD
                    ):
                        good_cheats.append((s_r, s_c, e_r, e_c))

            print(len(good_cheats))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv
import sys
from typing import Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
TURN_SCORE = 1000
FORWARD_SCORE = 1


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []

    def dfs(
        self, start: Tuple[int, int], end: Tuple[int, int], start_dir_idx: int
    ) -> int:
        """Uses DFS to find the lowest score needed to reach end from start.

        Moves will only be added to DFS stack if they are better than
        previously traversed move states.
        """
        min_cache = [
            [[sys.maxsize for _ in range(len(DIRS))] for _ in range(len(self.grid[0]))]
            for _ in range(len(self.grid))
        ]

        min_cache[start[0]][start[1]][start_dir_idx] = 0
        st = [(start[0], start[1], start_dir_idx, 0)]

        def handle_move(r: int, c: int, dir_idx: int, turn_idx: int, score: int):
            new_dir_idx = (dir_idx + turn_idx) % len(DIRS)
            d_r, d_c = DIRS[new_dir_idx]
            new_r, new_c = r + d_r, c + d_c
            new_score = (
                score + TURN_SCORE + FORWARD_SCORE
                if turn_idx != 0
                else score + FORWARD_SCORE
            )

            if self.grid[new_r][new_c] == ".":
                # Prune paths that won't beat optimal path
                if new_score >= min_cache[end[0]][end[1]][0]:
                    return
                elif new_score < min_cache[new_r][new_c][new_dir_idx]:
                    min_cache[new_r][new_c][new_dir_idx] = new_score
                    st.append((new_r, new_c, new_dir_idx, new_score))
            elif self.grid[new_r][new_c] == "E":
                min_cache[new_r][new_c][new_dir_idx] = min(
                    min_cache[new_r][new_c][new_dir_idx], new_score
                )

        while st:
            r, c, dir_idx, score = st.pop()

            # Handle left turn
            handle_move(r, c, dir_idx, len(DIRS) - 1, score)
            # Handle right turn
            handle_move(r, c, dir_idx, 1, score)
            # Handle forward
            handle_move(r, c, dir_idx, 0, score)

        # Direction not important for destination
        return min(min_cache[end[0]][end[1]])

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            start = (-1, -1)
            end = (-1, -1)

            for r_idx, row in enumerate(csv_reader):
                new_row = []

                for c_idx, c in enumerate(row[0]):
                    if c == "S":
                        start = (r_idx, c_idx)
                    elif c == "E":
                        end = (r_idx, c_idx)

                    new_row.append(c)

                self.grid.append(new_row)

            print(self.dfs(start, end, 1))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

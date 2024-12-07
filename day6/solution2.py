#! /usr/bin/python3.12
import csv
from copy import deepcopy
from typing import List, Set, Tuple

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.start = (-1, -1)

    def is_valid_position(self, grid: List[List[str]], r: int, c: int) -> bool:
        """Returns whether the given r,c is within grid bounds."""
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def traverse(
        self,
        grid: List[List[str]],
        r: int,
        c: int,
        direction_idx: int,
        added_obstacle: bool,
        seen_walls: Set[Tuple[int, int, int]] = set(),
    ) -> int:
        """Travels through grid, counting # of objects that cause loops.

        Inputs:
            grid: The grid created from the day's input. If called with
                `added_obstacle` = True, this will also contain an additional
                wall (character "o").
            r: Starting row (y) coordinate.
            c: Starting column (x) coordinate.
            direction_idx: The index corresponding to which direction in DIRS
                the guard is currently facing.
            added_obstacle: If True, indicates that an obstacle has been placed
                already, and termination condition is finding a loop or out of
                bounds.
            seen_walls: All (wall_r, wall_c, direction_idx) tuples that have
                already been seen during traversal. Tracked separately for
                added_obstacle = True vs. False, but is copied to pass in for
                recursive calls.

        Outputs:
            In added_obstacle = True: 1 if placed obstacle causes a loop or 0
                if not.
            In added_obstacle = False: Number of obstacles that can cause
                loops if placed.
        """
        attempted_obstacles = set([self.start])
        loop_obstacles = set()

        while True:
            d_r, d_c = DIRS[direction_idx]
            new_r, new_c = r + d_r, c + d_c

            if not self.is_valid_position(grid, new_r, new_c):
                break
            elif grid[new_r][new_c] == "#" or grid[new_r][new_c] == "o":
                if (new_r, new_c, direction_idx) in seen_walls:
                    return 1
                seen_walls.add((new_r, new_c, direction_idx))
                direction_idx = (direction_idx + 1) % len(DIRS)
            else:
                # New attempted obstacle placement along visited path.
                if not added_obstacle and (new_r, new_c) not in attempted_obstacles:
                    grid[new_r][new_c] = "o"
                    if self.traverse(
                        grid, r, c, direction_idx, True, seen_walls.copy()
                    ):
                        loop_obstacles.add((new_r, new_c))
                    attempted_obstacles.add((new_r, new_c))
                    grid[new_r][new_c] = "."
                r, c = (new_r, new_c)

        return len(loop_obstacles)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            grid = []
            direction_idx = 0

            for row in csv_reader:
                new_row = []
                for idx, c in enumerate(row[0]):
                    if c == "^":
                        self.start = (len(grid), idx)
                    new_row.append(c)

                grid.append(new_row)

            print(
                self.traverse(grid, self.start[0], self.start[1], direction_idx, False)
            )


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

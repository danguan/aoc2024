#! /usr/bin/python3.12
import csv
import numpy as np
import re
from typing import List, Tuple

A_COST = 3
B_COST = 1
MAX_PRESSES = 100
ERROR_CONST = 10000000000000


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_optimal_game_cost(self, game: List[Tuple[int, int]]) -> int:
        """Returns optimal game cost using linear system of equations.

        Delegates to numpy module to solve system of equations and rounds
        final result with a check to confirm that rounded results will produce
        correct prize coordinate.
        """
        (a_x, a_y), (b_x, b_y), (t_x, t_y) = game
        left = np.array([[a_x, b_x], [a_y, b_y]])
        right = np.array([t_x, t_y])
        solution = np.linalg.solve(left, right)

        rounded_a_presses = solution[0].round().astype(int)
        rounded_b_presses = solution[1].round().astype(int)

        if (
            rounded_a_presses * a_x + rounded_b_presses * b_x == t_x
            and rounded_a_presses * a_y + rounded_b_presses * b_y == t_y
        ):
            return A_COST * rounded_a_presses + B_COST * rounded_b_presses

        return 0

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            games = []
            total_cost = 0

            for row in csv_reader:
                if not row:
                    continue
                elif a_match := re.search(
                    r"Button A: X\+(\d+), Y\+(\d+)", ",".join(row)
                ):
                    games.append([(int(a_match.group(1)), int(a_match.group(2)))])
                elif b_match := re.search(
                    r"Button B: X\+(\d+), Y\+(\d+)", ",".join(row)
                ):
                    games[-1].append((int(b_match.group(1)), int(b_match.group(2))))
                elif prize_match := re.search(
                    r"Prize: X=(\d+), Y=(\d+)", ",".join(row)
                ):
                    games[-1].append(
                        (
                            ERROR_CONST + int(prize_match.group(1)),
                            ERROR_CONST + int(prize_match.group(2)),
                        )
                    )

            for game in games:
                total_cost += self.get_optimal_game_cost(game)

            print(total_cost)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

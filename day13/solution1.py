#! /usr/bin/python3.12
import csv
import re
import sys
from typing import List, Tuple

A_COST = 3
B_COST = 1
MAX_PRESSES = 100


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_optimal_game_cost(self, game: List[Tuple[int, int]]) -> int:
        """Brute forces minimum game cost for given game if possible.

        If no possible solution is found, should return 0.
        """
        min_cost = sys.maxsize

        (a_x, a_y), (b_x, b_y), (t_x, t_y) = game
        for a_presses in range(MAX_PRESSES + 1):
            for b_presses in range(MAX_PRESSES + 1):
                total_x = a_x * a_presses + b_x * b_presses
                total_y = a_y * a_presses + b_y * b_presses

                if total_x > t_x or total_y > t_y:
                    break
                elif total_x == t_x and total_y == t_y:
                    min_cost = min(min_cost, A_COST * a_presses + B_COST * b_presses)

        return min_cost if min_cost != sys.maxsize else 0

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
                        (int(prize_match.group(1)), int(prize_match.group(2)))
                    )

            for game in games:
                total_cost += self.get_optimal_game_cost(game)

            print(total_cost)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

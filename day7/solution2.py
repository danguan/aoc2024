#! /usr/bin/python3.12
import csv
from typing import List

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def can_reach_target(
        self, nums: List[int], idx: int, curr_val: int, target: int
    ) -> bool:
        """+/*/|| curr_val with nums to see if target is reachable.

        Recursively either adds, multiplies, or concats curr_val with the num
        at given `idx` in `nums` until all numbers have been processed, in
        order.
        """
        if idx == len(nums):
            if curr_val == target:
                return True
            return False
        elif curr_val > target:
            return False

        return (
            self.can_reach_target(nums, idx + 1, curr_val + nums[idx], target)
            or self.can_reach_target(nums, idx + 1, curr_val * nums[idx], target)
            or self.can_reach_target(
                nums, idx + 1, int(str(curr_val) + str(nums[idx])), target
            )
        )

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_calibration_result = 0

            for row in csv_reader:
                equation = row[0].split(":")
                target = int(equation[0])
                nums = [int(num) for num in equation[1].split(" ")[1:]]

                if self.can_reach_target(nums, 1, nums[0], target):
                    total_calibration_result += target

            print(total_calibration_result)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

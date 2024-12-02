#! /usr/bin/python3.12
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def is_report_safe(self, report: List[int]) -> bool:
        """Check if given report has acceptable diffs between levels.

        Acceptible is defined by problem statement as between 1 and 3 inclusive
        in either direction as long as the direction is consistent per report.
        """
        is_inc = report[1] > report[0]

        for idx in range(1, len(report)):
            level_diff = (
                report[idx] - report[idx - 1]
                if is_inc
                else report[idx - 1] - report[idx]
            )
            if level_diff < 1 or level_diff > 3:
                return False

        return True

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            safe_reports = 0

            for row in csv_reader:
                report = [int(num) for num in row[0].split(" ")]
                is_report_safe = self.is_report_safe(report)

                if is_report_safe is True:
                    safe_reports += 1
                else:
                    for broken_idx in range(len(report)):
                        if self.is_report_safe(
                            report[:broken_idx] + report[broken_idx + 1 :]
                        ):
                            safe_reports += 1
                            break

            print(safe_reports)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

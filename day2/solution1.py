#! /usr/bin/python3.12
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            safe_reports = 0

            for row in csv_reader:
                is_safe = True
                report = [int(num) for num in row[0].split(" ")]
                is_inc = report[1] > report[0]

                for idx in range(1, len(report)):
                    level_diff = report[idx] - report[idx - 1] if is_inc else report[idx - 1] - report[idx]
                    if level_diff < 1 or level_diff > 3:
                        is_safe = False
                        break

                if is_safe:
                    safe_reports += 1
            
            print(safe_reports)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

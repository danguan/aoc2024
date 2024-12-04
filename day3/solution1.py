#! /usr/bin/python3.12
import csv
import re

class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            mul_total = 0
            mul_pattern = r"mul\(\d+,\d+\)"

            for row in csv_reader:
                muls = re.findall(mul_pattern, ",".join(row))

                for mul in muls:
                    curr_total = 1
                    num_pattern = r"\d+"
                    for num in re.findall(num_pattern, mul):
                        curr_total *= int(num)
                    
                    mul_total += curr_total

            print(mul_total)
            


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

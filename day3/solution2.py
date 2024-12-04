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
            curr_do = True
            do_pattern = r"do\(\)"
            dont_pattern = r"don't\(\)"

            for row in csv_reader:
                matches = re.findall(
                    re.compile("(%s|%s|%s)" % (mul_pattern, do_pattern, dont_pattern)),
                    ",".join(row),
                )

                for match in matches:
                    if re.match(do_pattern, match):
                        curr_do = True
                    elif re.match(dont_pattern, match):
                        curr_do = False
                    elif curr_do:
                        curr_total = 1
                        num_pattern = r"\d+"
                        for num in re.findall(num_pattern, match):
                            curr_total *= int(num)
                        mul_total += curr_total

            print(mul_total)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

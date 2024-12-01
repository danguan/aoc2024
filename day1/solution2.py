#! /usr/bin/python3.12
import csv
from collections import defaultdict


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_similarity = 0
            counts_a = defaultdict(int)
            counts_b = defaultdict(int)

            for row in csv_reader:
                num_a, num_b = row[0].split("   ")
                counts_a[int(num_a)] += 1
                counts_b[int(num_b)] += 1

            for k, v in counts_a.items():
                total_similarity += k * v * counts_b[k]

            print(total_similarity)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

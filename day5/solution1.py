#! /usr/bin/python3.12
import csv
import re
from collections import defaultdict
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.adj = defaultdict(list)

    def is_valid_page(self, page: List[int]) -> bool:
        """Returns whether given page is valid based on page ordering rules."""

        for idx in range(len(page) - 1):
            for pair_idx in range(idx + 1, len(page)):
                # Explicitly violates a page ordering rule
                if page[idx] in self.adj[page[pair_idx]]:
                    return False

        return True

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_centers = 0
            order_pattern = r"\d+\|\d+"
            pages = []

            for row in csv_reader:
                if not row:
                    continue
                if re.match(order_pattern, row[0]):
                    src, dst = row[0].split("|")
                    self.adj[int(src)].append(int(dst))
                else:
                    pages.append([int(num) for num in row])

            for page in pages:
                if self.is_valid_page(page):
                    total_centers += page[len(page) // 2]

            print(total_centers)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

#! /usr/bin/python3.12
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_difference = 0
            list_a = []
            list_b = []

            for row in csv_reader:
                num_a, num_b = row[0].split("   ")
                list_a.append(int(num_a))
                list_b.append(int(num_b))
            
            list_a.sort()
            list_b.sort()

            for item_a, item_b in zip(list_a, list_b):
                total_difference += abs(item_a - item_b)

            print(total_difference)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

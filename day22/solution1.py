#! /usr/bin/python3.12
import csv

FINAL_SECRET_NUMBER = 2000
MOD = 16777216


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_new_secret_number(self, initial_num: int, new_num_count: int) -> int:
        """Finds the secret number `new_num_count` nums from initial_num."""
        curr_secret_num = initial_num

        for _ in range(new_num_count):
            curr_secret_num ^= curr_secret_num * 64
            curr_secret_num %= MOD
            curr_secret_num ^= curr_secret_num // 32
            curr_secret_num %= MOD
            curr_secret_num ^= curr_secret_num * 2048
            curr_secret_num %= MOD

        return curr_secret_num

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            secret_numbers = []
            total_secret_numbers = 0

            for row in csv_reader:
                secret_numbers.append(int(row[0]))

            for secret_number in secret_numbers:
                total_secret_numbers += self.get_new_secret_number(
                    secret_number, FINAL_SECRET_NUMBER
                )

            print(total_secret_numbers)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

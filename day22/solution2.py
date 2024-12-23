#! /usr/bin/python3.12
import csv
from collections import defaultdict, deque
from typing import List

FINAL_SECRET_NUMBER = 2000
MOD = 16777216
WINDOW_LEN = 4


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.sequences = defaultdict(int)

    def get_prices(self, initial_num: int, new_num_count: int) -> List[int]:
        """Finds all prices from `initial_num` up to `new_num_count` prices."""
        curr_secret_num = initial_num
        prices = [curr_secret_num % 10]

        for _ in range(new_num_count):
            curr_secret_num ^= curr_secret_num * 64
            curr_secret_num %= MOD
            curr_secret_num ^= curr_secret_num // 32
            curr_secret_num %= MOD
            curr_secret_num ^= curr_secret_num * 2048
            curr_secret_num %= MOD
            prices.append(curr_secret_num % 10)

        return prices

    def populate_sequences(self, price_list: List[int]):
        """Accumulates total bananas per first view of sequence in price_list.

        Maintains seen sequences to prevent double-counting a sequence within
        the same price list.
        """
        window = deque([-1])
        right = 1
        seen_sequences = set()

        while right < WINDOW_LEN:
            window.append(price_list[right] - price_list[right - 1])
            right += 1

        while right < len(price_list):
            window.popleft()
            window.append(price_list[right] - price_list[right - 1])

            t_window = tuple(window)

            if t_window not in seen_sequences:
                seen_sequences.add(t_window)
                self.sequences[t_window] += price_list[right]

            right += 1

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            secret_numbers = []
            all_prices = []

            for row in csv_reader:
                secret_numbers.append(int(row[0]))

            for secret_number in secret_numbers:
                all_prices.append(self.get_prices(secret_number, FINAL_SECRET_NUMBER))

            for price_list in all_prices:
                self.populate_sequences(price_list)

            print(max(self.sequences.values()))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

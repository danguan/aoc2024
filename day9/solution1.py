#! /usr/bin/python3.12
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            disk_map = ""

            for row in csv_reader:
                # 0 spaces for last number in disk_map
                disk_map = row[0] + "0"

            mapped_arr = []
            checksum = 0
            curr_id = 0
            file_counts = []
            no_gap_file_max_len = 0

            for idx in range(0, len(disk_map), 2):
                file_counts.append([curr_id, int(disk_map[idx])])
                no_gap_file_max_len += int(disk_map[idx])
                mapped_arr.extend([file_counts[-1][0] for _ in range(file_counts[-1][1])])
                mapped_arr.extend(["." for _ in range(int(disk_map[idx + 1]))])
                curr_id += 1

            for idx in range(no_gap_file_max_len):
                if mapped_arr[idx] == ".":
                    mapped_arr[idx] = file_counts[-1][0]
                    file_counts[-1][1] -= 1
                    if file_counts[-1][1] == 0:
                        file_counts.pop()
                checksum += mapped_arr[idx] * idx

            print(checksum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

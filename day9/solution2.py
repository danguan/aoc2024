#! /usr/bin/python3.12
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def sub_checksum(self, id: int, start_pos: int, end_pos: int) -> int:
        """Returns checksum for given ID between [start_pos, end_pos).
        
        Based on formula of ((n * (n + 1)) // 2) to get sum of all numbers in
        range [1, n].
        """
        return (
            ((end_pos - 1) * end_pos // 2) - ((start_pos - 1) * start_pos // 2)
        ) * id

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            disk_map = ""

            for row in csv_reader:
                # 0 spaces for last number in disk_map
                disk_map = row[0] + "0"

            checksum = 0
            curr_id = 0
            # ID, size, position, moved
            file_counts_pos_moved = []
            # Size, position, moved
            gap_counts_pos_moved = []
            mapped_arr_idx = 0

            for idx in range(0, len(disk_map), 2):
                file_counts_pos_moved.append(
                    [curr_id, int(disk_map[idx]), mapped_arr_idx, False]
                )
                mapped_arr_idx += file_counts_pos_moved[-1][1]
                gap_counts_pos_moved.append(
                    [int(disk_map[idx + 1]), mapped_arr_idx, []]
                )
                mapped_arr_idx += gap_counts_pos_moved[-1][0]
                curr_id += 1

            for f_idx in range(len(file_counts_pos_moved) - 1, 0, -1):
                f_id, f_size, f_pos, f_moved = file_counts_pos_moved[f_idx]
                for g_idx in range(f_idx):
                    g_size, g_pos, g_moved = gap_counts_pos_moved[g_idx]
                    if f_size <= g_size:
                        # Set file moved = True
                        file_counts_pos_moved[f_idx][3] = True
                        # Reduce available gap count at g_idx
                        gap_counts_pos_moved[g_idx][0] -= f_size
                        # Add ID and size of moved file to g_idx
                        gap_counts_pos_moved[g_idx][2].append((f_id, f_size))
                        break

            for f_g_idx in range(len(file_counts_pos_moved)):
                f_id, f_size, f_pos, f_moved = file_counts_pos_moved[f_g_idx]
                _, g_pos, g_moved = gap_counts_pos_moved[f_g_idx]
                # Add sub_checksum for any non-moved files
                if f_moved is False:
                    checksum += self.sub_checksum(f_id, f_pos, f_pos + f_size)

                # Add sub_checksum for any moved files
                if g_moved:
                    curr_moved_size = 0
                    for id, size in g_moved:
                        checksum += self.sub_checksum(
                            id,
                            g_pos + curr_moved_size,
                            g_pos + curr_moved_size + size,
                        )
                        curr_moved_size += size

            print(checksum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

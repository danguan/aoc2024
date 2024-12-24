#! /usr/bin/python3.12
import csv
from collections import defaultdict
from typing import DefaultDict, List, Set, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def find_connected_computers(
        self, adj: DefaultDict[str, Set[str]]
    ) -> Set[Tuple[str, str, str]]:
        s_adj_keys = list(adj.keys())
        s_adj_keys.sort()
        connected_computers = set()

        for i in range(len(s_adj_keys) - 2):
            i_k = s_adj_keys[i]
            for j in range(i + 1, len(s_adj_keys) - 1):
                j_k = s_adj_keys[j]
                for k in range(j + 1, len(s_adj_keys)):
                    k_k = s_adj_keys[k]

                    if (
                        (i_k in adj[j_k] and i_k in adj[k_k])
                        and (j_k in adj[i_k] and j_k in adj[k_k])
                        and (k_k in adj[i_k] and k_k in adj[j_k])
                    ):
                        connected_computers.add((i_k, j_k, k_k))

        return connected_computers

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            adj = defaultdict(set)

            for row in csv_reader:
                src, dst = row[0].split("-")
                adj[src].add(dst)
                adj[dst].add(src)

            connected_computers = self.find_connected_computers(adj)
            t_computer_groups = 0

            for c1, c2, c3 in connected_computers:
                if c1[0] == "t" or c2[0] == "t" or c3[0] == "t":
                    t_computer_groups += 1

            print(t_computer_groups)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

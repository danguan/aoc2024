#! /usr/bin/python3.12
import csv
from collections import defaultdict
from typing import DefaultDict, List, Set, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def bors_kerbosch_v1(self, R, P, X, G, C):
        if len(P) == 0 and len(X) == 0:
            if len(R) > 2:
                C.append(sorted(R))
            return

        for v in P.union(set([])):
            self.bors_kerbosch_v1(
                R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C
            )
            P.remove(v)
            X.add(v)

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            adj = defaultdict(set)

            for row in csv_reader:
                src, dst = row[0].split("-")
                adj[src].add(dst)
                adj[dst].add(src)

            biggest_cliques = []
            self.bors_kerbosch_v1(set(), set(adj.keys()), set(), adj, biggest_cliques)
            biggest_clique = ([], 0)

            for clique in biggest_cliques:
                if len(clique) > biggest_clique[1]:
                    biggest_clique = (clique, len(clique))

            print(",".join(biggest_clique[0]))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

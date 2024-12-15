#! /usr/bin/python3.12
import csv

DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.grid = []
        self.moves = []
        self.start = (-1, -1)

    def get_box_coords(self) -> int:
        """Finds the total value of all box GPS coordinates."""
        total_box_coords = 0

        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                # Going top left to bottom right, should always see left
                # bracket of box first before right bracket
                if self.grid[r][c] == "[":
                    total_box_coords += (100 * r) + c

        return total_box_coords

    def do_moves(self):
        """Simulate all of `self.moves` in place on `self.grid`.

        Pushing boxes entails finding first empty space and switching box with
        empty space, then moving forwards.
        """
        r, c = self.start

        def handle_up_down(r: int, c: int, d_r: int, d_c: int):
            """Moves boxes up or down based on input `d_r` and `d_c` direction.

            Assumes box position is already valid based on
            `can_move_up_down()`.
            """
            new_r, new_c = r + d_r, c + d_c

            if self.grid[r][c] == ".":
                return
            elif self.grid[r][c] == "[":
                handle_up_down(new_r, new_c, d_r, d_c)
                handle_up_down(new_r, new_c + 1, d_r, d_c)
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[new_r][new_c + 1] = self.grid[r][c + 1]
                self.grid[r][c] = "."
                self.grid[r][c + 1] = "."
            elif self.grid[r][c] == "]":
                handle_up_down(new_r, new_c, d_r, d_c)
                handle_up_down(new_r, new_c - 1, d_r, d_c)
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[new_r][new_c - 1] = self.grid[r][c - 1]
                self.grid[r][c] = "."
                self.grid[r][c - 1] = "."

        def can_move_up_down(r: int, c: int, d_r: int, d_c: int) -> bool:
            """Checks whether box at r,c can be moved up or down.

            Uses input `d_r` and `d_c` to determine direction, and recursively
            checks for any possible wall blockages along the way."""
            new_r, new_c = r + d_r, c + d_c

            if self.grid[r][c] == ".":
                return True
            elif self.grid[r][c] == "#":
                return False
            elif self.grid[r][c] == "[":
                return can_move_up_down(new_r, new_c, d_r, d_c) and can_move_up_down(
                    new_r, new_c + 1, d_r, d_c
                )
            elif self.grid[r][c] == "]":
                return can_move_up_down(new_r, new_c, d_r, d_c) and can_move_up_down(
                    new_r, new_c - 1, d_r, d_c
                )

            # Should never reach here
            return False

        def handle_left_right(r: int, c: int, d_c: int) -> bool:
            """Moves boxes left or right based on input `d_c` direction.

            Since boxes are only wider and not taller, do not need to
            recursively check whether input box may affect 2 other spaces.
            """
            # new_c here needs to be 2 * d_c to accommodate for wider boxes
            new_c = c + 2 * d_c

            if self.grid[r][c] == ".":
                return True
            elif self.grid[r][c] == "#":
                return False
            elif self.grid[r][c] in ["[", "]"]:
                if handle_left_right(r, new_c, d_c):
                    self.grid[r][new_c] = self.grid[r][c + d_c]
                    self.grid[r][c + d_c] = self.grid[r][c]
                    self.grid[r][c] = "."
                    return True

                return False

            # Should never reach here
            return False

        for move in self.moves:
            d_r, d_c = DIRS[move]
            new_r, new_c = r + d_r, c + d_c

            # Wall
            if self.grid[new_r][new_c] == "#":
                continue
            # Box
            elif self.grid[new_r][new_c] in ["[", "]"]:
                if move in ["^", "v"]:
                    if can_move_up_down(new_r, new_c, d_r, d_c):
                        handle_up_down(new_r, new_c, d_r, d_c)
                elif move in ["<", ">"]:
                    handle_left_right(new_r, new_c, d_c)

            # Empty space
            if self.grid[new_r][new_c] == ".":
                self.grid[r][c] = "."
                self.grid[new_r][new_c] = "@"
                r, c = new_r, new_c

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            grid = True

            for row_idx, row in enumerate(csv_reader):
                if not row:
                    grid = False
                elif row and grid:
                    grid_row = []
                    for idx, c in enumerate(row[0]):
                        if c == "@":
                            self.start = (row_idx, 2 * idx)
                            grid_row.extend(["@", "."])
                        elif c == "O":
                            grid_row.extend(["[", "]"])
                        else:
                            grid_row.extend([c, c])
                    self.grid.append(grid_row)
                else:
                    self.moves.extend([c for c in row[0]])

            self.do_moves()
            print(self.get_box_coords())


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

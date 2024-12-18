#! /usr/bin/python3.12
import csv
import re
from typing import List

INSTRUCTIONS = {
    "adv": 0,
    "bxl": 1,
    "bst": 2,
    "jnz": 3,
    "bxc": 4,
    "out": 5,
    "bdv": 6,
    "cdv": 7,
}


class Solution(object):
    def __init__(self, filename):
        self.filename = filename
        self.a = -1
        self.b = -1
        self.c = -1

    def get_combo_op(self, op: int) -> int:
        """Returns combo operand value for given operand."""
        if op == 0:
            return 0
        elif op == 1:
            return 1
        elif op == 2:
            return 2
        elif op == 3:
            return 3
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        elif op == 7:
            raise NotImplementedError("Reserved")

    def handle_instruction(self, ins: int, op: int) -> int:
        """Interprets specific instruction types and applies their outputs."""
        if ins == INSTRUCTIONS["adv"]:
            self.a //= 2 ** self.get_combo_op(op)
        elif ins == INSTRUCTIONS["bxl"]:
            self.b ^= op
        elif ins == INSTRUCTIONS["bst"]:
            self.b = self.get_combo_op(op) % 8
        elif ins == INSTRUCTIONS["bxc"]:
            self.b ^= self.c
        elif ins == INSTRUCTIONS["out"]:
            return self.get_combo_op(op) % 8
        elif ins == INSTRUCTIONS["bdv"]:
            self.b = self.a // (2 ** self.get_combo_op(op))
        elif ins == INSTRUCTIONS["cdv"]:
            self.c = self.a // (2 ** self.get_combo_op(op))

        return -1

    def run_program(self, program: List[int]) -> List[int]:
        """Runs input program based on problem-defined operations.

        Returns output after all operations have been applied.
        """
        curr_idx = 0
        output = []

        while curr_idx < len(program):
            instruction, operand = program[curr_idx], program[curr_idx + 1]

            if instruction == INSTRUCTIONS["jnz"] and self.a != 0:
                curr_idx = operand
            else:
                out = self.handle_instruction(instruction, operand)

                if instruction == INSTRUCTIONS["out"]:
                    output.append(out)

                curr_idx += 2

        return output

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            program = []

            for row in csv_reader:
                if not row:
                    continue
                elif a_match := re.search(r"Register A: (\d+)", ",".join(row)):
                    self.a = int(a_match.group(1))
                elif b_match := re.search(r"Register B: (\d+)", ",".join(row)):
                    self.b = int(b_match.group(1))
                elif c_match := re.search(r"Register C: (\d+)", ",".join(row)):
                    self.c = int(c_match.group(1))
                elif program_match := re.search(r"Program: ((\d,*)+)", ",".join(row)):
                    program = [int(num) for num in program_match.group(1).split(",")]

            def find_solution_a_value(idx: int, curr_val: int) -> int:
                """Helper to find lowest a_value that produces program.

                The key insight here is that the given input program is a loop
                that applies several operations, then outputs a value, then
                loops back to the initial instruction.

                Looking at the instructions, the operations pertain primarily
                to the last 3 bits of self.a each time, as after each loop,
                we divide self.a by 8, i.e. >> 3. This helper can thus look to
                find the `val` that produces the program at each slice, and
                build on that value to produce the full program.

                The slices are incremented on, in reverse order, as we consider
                the last 3 bits of self.a for each iteration. For example, if
                the value was (in binary) 111000, the output of applying the
                program on would be similar to [program(000), program(111)].
                Extrapolating, to build the output in correct order, we need
                to iterate through all indices backwards.
                """
                for val in range(8):
                    self.a = (curr_val << 3) + val
                    self.b = 0
                    self.c = 0
                    output = self.run_program(program)

                    # Found matching output/program
                    if output == program[idx:]:
                        if idx == 0:
                            return (curr_val << 3) + val

                        sub_output = find_solution_a_value(
                            idx - 1, (curr_val << 3) + val
                        )
                        if sub_output != -1:
                            return sub_output
                return -1

            print(find_solution_a_value(len(program) - 1, 0))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()

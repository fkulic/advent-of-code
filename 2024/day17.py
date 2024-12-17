from copy import deepcopy
import sys
from pathlib import Path


class Computer:
    def __init__(self, registers: dict[str, int], instructions: list[int]) -> None:
        self.instruction_pointer = 0
        self.instructions = instructions
        self.registers = registers
        self._out = []

    def reset(self, registers: dict[str, int]) -> None:
        self.instruction_pointer = 0
        self._out = []
        self.registers = registers

    def get_operand(self, combo_operand: int) -> int:
        if combo_operand <= 3:
            return combo_operand
        elif combo_operand == 4:
            return self.registers["A"]
        elif combo_operand == 5:
            return self.registers["B"]
        elif combo_operand == 6:
            return self.registers["C"]
        else:
            raise Exception("PROGRAM NOT VALId")

    def execute_all(self) -> str:
        while self.instruction_pointer < len(self.instructions):
            self.execute_instruction()
        return ",".join(map(str, self._out))

    def execute_instruction(self) -> None:
        ip = self.instruction_pointer
        instruction = self.instructions[ip]
        operand = self.instructions[ip + 1]
        match instruction:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                self.jnz(operand)
            case 4:
                self.bxc(operand)
            case 5:
                self.out(operand)
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)
        if ip == self.instruction_pointer:
            self.instruction_pointer += 2

    def adv(self, combo_operand: int) -> None:  # 0
        self.registers["A"] = self.registers["A"] // 2 ** self.get_operand(combo_operand)

    def bxl(self, operand: int) -> None:  # 1
        self.registers["B"] = self.registers["B"] ^ operand

    def bst(self, combo_operand: int) -> None:  # 2
        self.registers["B"] = self.get_operand(combo_operand) % 8

    def jnz(self, operand: int) -> None:  # 3
        if self.registers["A"] == 0:
            return
        self.instruction_pointer = operand

    def bxc(self, operand: int) -> None:  # 4
        # ignore operand and use registers only
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]

    def out(self, combo_operand: int) -> None:  # 5
        self._out.append(self.get_operand(combo_operand) % 8)

    def bdv(self, combo_operand: int) -> None:  # 6
        self.registers["B"] = self.registers["A"] // (2 ** self.get_operand(combo_operand))

    def cdv(self, combo_operand: int) -> None:  # 7
        self.registers["C"] = self.registers["A"] // (2 ** self.get_operand(combo_operand))


def part_one(registers, instructions) -> str:
    pc = Computer(deepcopy(registers), instructions)
    return pc.execute_all()


def calc(a):
    # Specific for my input
    b = a % 8
    b ^= 1
    c = a // (2**b)
    b = (b ^ c) ^ 4
    return b


def get_output(a, r=None):
    if r is None:
        r = []
    if a == 0:
        return r
    else:
        b = calc(a)
        r.append(b % 8)
        return get_output(a // 8, r)


def compare_with_instructions(a):
    count = 0
    for i in range(len(a)):
        if a[i] == INSTRUCTIONS[i]:
            count += 1
        else:
            return count
    return count


def part_two() -> int:
    a = 0
    n = 0
    while True:
        # new_a = a * 8**5 + 0o25052 # 0o125052, 0o225052, 0o325052, ...
        # new_a = a * 8**9 + 0o654025052
        new_a = a * 8**12 + 0o647654025052
        res = get_output(new_a)
        matched_numbers = compare_with_instructions(res)
        if matched_numbers > n:
            n = matched_numbers
            # print(oct(new_a), new_a, matched_numbers)
            if matched_numbers == len(INSTRUCTIONS):
                return new_a
        else:
            a += 1


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    r, p = input_path.read_text().strip().split("\n\n")

    registers = {}
    for line in r.splitlines():
        splitted = line.split()
        registers[splitted[1][0]] = int(splitted[-1])

    INSTRUCTIONS = [int(x) for x in p.split()[-1].split(",")]

    print("FIRST PART", part_one(registers, INSTRUCTIONS))
    print("SECOND PART", part_two())

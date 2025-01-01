import sys
from pathlib import Path


REGISTERS = {"a": 0, "b": 0}


def execute_instructions(instructions: list[tuple[str, ...]]):
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        instruction = instructions[instruction_pointer]
        match instruction[0]:
            case "hlf":
                REGISTERS[instruction[1]] //= 2
                instruction_pointer += 1
            case "tpl":
                REGISTERS[instruction[1]] *= 3
                instruction_pointer += 1
            case "inc":
                REGISTERS[instruction[1]] += 1
                instruction_pointer += 1
            case "jmp":
                instruction_pointer += int(instruction[1])
            case "jie":
                if REGISTERS[instruction[1]] % 2 == 0:
                    instruction_pointer += int(instruction[2])
                else:
                    instruction_pointer += 1
            case "jio":
                if REGISTERS[instruction[1]] == 1:
                    instruction_pointer += int(instruction[2])
                else:
                    instruction_pointer += 1


def part_one(instructions: list[tuple[str, list[str]]]) -> int:
    execute_instructions(instructions)
    return REGISTERS["b"]


def part_two(instructions) -> int:
    REGISTERS["a"] = 1
    REGISTERS["b"] = 0
    execute_instructions(instructions)
    return REGISTERS["b"]


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    instructions = []
    for line in input_path.read_text().splitlines():
        instruction, *args = [s.removesuffix(",") for s in line.split(" ")]
        instructions.append((instruction, *args))

    print("FIRST PART", part_one(instructions))
    print("SECOND PART", part_two(instructions))

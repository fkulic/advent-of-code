from copy import deepcopy
import functools
import operator
from enum import Enum


class Instruction(Enum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_REL_BASE = 9
    HALT = 99


NUM_ARGS = {
    Instruction.ADD: (2, 1),
    Instruction.MUL: (2, 1),
    Instruction.INPUT: (0, 1),
    Instruction.OUTPUT: (1, 0),
    Instruction.JUMP_IF_TRUE: (2, 0),
    Instruction.JUMP_IF_FALSE: (2, 0),
    Instruction.LESS_THAN: (2, 1),
    Instruction.EQUALS: (2, 1),
    Instruction.ADJUST_REL_BASE: (1, 0),
    Instruction.HALT: (0, 0),
}


class ArgumentMode(Enum):
    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2


class IntCodeComputer:

    def __init__(self, memory: list[int], input_function, output_function=None) -> None:
        self._ip = 0
        self._memory = memory
        self._input_function = input_function
        self._output = []
        out_function = output_function if output_function else self._output_function
        self._relative_base = 0
        self._write_idx = 0
        self._operations = {
            Instruction.ADD: self._wrap_math(operator.add),
            Instruction.MUL: self._wrap_math(operator.mul),
            Instruction.OUTPUT: out_function,
            Instruction.INPUT: self._wrapped_input_function,
            Instruction.JUMP_IF_TRUE: self._jump_if_true,
            Instruction.JUMP_IF_FALSE: self._jump_if_false,
            Instruction.LESS_THAN: self._wrap_math(operator.lt),
            Instruction.EQUALS: self._wrap_math(operator.eq),
            Instruction.ADJUST_REL_BASE: self._adjust_rel_base,
        }

    def clone(self, input_function, output_function=None):
        new_instance = IntCodeComputer(
            deepcopy(self._memory),
            input_function,
            output_function,
        )
        new_instance._ip = self._ip
        new_instance._relative_base = self._relative_base
        new_instance._output = deepcopy(self._output)
        return new_instance

    def _check_and_extend(self, idx):
        diff = idx - len(self._memory) + 1
        if diff > 0:
            self._memory.extend([0 for _ in range(diff)])

    def _write_to_memory(self, value):
        assert self._write_idx is not None
        self._check_and_extend(self._write_idx)
        self._memory[self._write_idx] = value

    def _read_from_memory(self, idx):
        self._check_and_extend(idx)
        return self._memory[idx]

    def _wrap_math(self, fun):
        @functools.wraps(fun)
        def wrapped(*args):
            self._write_to_memory(int(fun(*args)))

        return wrapped

    def _output_function(self, arg):
        self._output.append(arg)

    def _jump_if_true(self, arg1, arg2):
        if arg1 != 0:
            self._jumped = True
            self._ip = arg2

    def _jump_if_false(self, arg1, arg2):
        if arg1 == 0:
            self._jumped = True
            self._ip = arg2

    def _adjust_rel_base(self, arg):
        self._relative_base += arg

    def _wrapped_input_function(self):
        if (value := self._input_function()) is not None:
            self._write_to_memory(value)
        else:
            return False

    def _get_in_args(self, n, modes):
        ins = []
        for i in range(0, n):
            value = self._read_from_memory(self._ip + i + 1)
            if modes[i] == ArgumentMode.POSITION_MODE:
                ins.append(self._read_from_memory(value))
            elif modes[i] == ArgumentMode.IMMEDIATE_MODE:
                ins.append(value)
            elif modes[i] == ArgumentMode.RELATIVE_MODE:
                ins.append(self._read_from_memory(self._relative_base + value))
            else:
                raise Exception("Unknown mode")
        return ins

    def _extract_mode_and_operation(self):
        instruction = self._memory[self._ip]
        op = Instruction(instruction % 100)
        c = ArgumentMode(instruction // 100 % 10)
        b = ArgumentMode(instruction // 1000 % 10)
        a = ArgumentMode(instruction // 10000 % 10)
        return op, [c, b, a]

    def _set_write_idx(self, op, modes):
        n_in, n_out = NUM_ARGS[op]
        if n_out > 0:
            output_idx = self._read_from_memory(self._ip + n_in + 1)
            if modes[n_in] == ArgumentMode.POSITION_MODE:
                self._write_idx = output_idx
            elif modes[n_in] == ArgumentMode.RELATIVE_MODE:
                self._write_idx = self._relative_base + output_idx
            else:
                raise Exception("Invalid mode for write index")
        else:
            self._write_idx = None

    def _execute_op(self):
        self._jumped = False
        op, modes = self._extract_mode_and_operation()
        n_in, n_out = NUM_ARGS[op]
        args = self._get_in_args(n_in, modes)
        self._set_write_idx(op, modes)
        if self._operations[op](*args) is False:
            return 0
        return 1 + n_in + n_out

    def run_intcode(self) -> bool:
        while self._memory[self._ip] != Instruction.HALT.value:
            if (n := self._execute_op()) == 0:
                break
            elif not self._jumped:
                self._ip += n
        return self._memory[self._ip] == Instruction.HALT.value

    @property
    def output(self):
        return self._output

import functools
import operator


class Instruction:
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


NUM_IN_ARGS = {
    Instruction.ADD: 2,
    Instruction.MUL: 2,
    Instruction.INPUT: 0,
    Instruction.OUTPUT: 1,
    Instruction.JUMP_IF_TRUE: 2,
    Instruction.JUMP_IF_FALSE: 2,
    Instruction.LESS_THAN: 2,
    Instruction.EQUALS: 2,
}


POSITION_MODE = 0


class IntCodeComputer:

    def __init__(self, memory: list[int], input_function) -> None:
        self._ip = 0
        self._memory = memory
        self._input_function = input_function
        self._output = []
        self._operations = {
            Instruction.ADD: self._wrap_math(operator.add),
            Instruction.MUL: self._wrap_math(operator.mul),
            Instruction.OUTPUT: self._output_function,
            Instruction.INPUT: self._wrapped_input_function,
            Instruction.JUMP_IF_TRUE: self._jump_if_true,
            Instruction.JUMP_IF_FALSE: self._jump_if_false,
            Instruction.LESS_THAN: self._wrap_math(operator.lt),
            Instruction.EQUALS: self._wrap_math(operator.eq),
        }

    def _wrap_math(self, fun):
        @functools.wraps(fun)
        def wrapped(*args):
            out_address = self._memory[self._ip]
            self._memory[out_address] = int(fun(*args))
            self._ip += 1

        return wrapped

    def _output_function(self, arg):
        self._output.append(arg)

    def _jump_if_true(self, arg1, arg2):
        if arg1 != 0:
            self._ip = arg2

    def _jump_if_false(self, arg1, arg2):
        if arg1 == 0:
            self._ip = arg2

    def _wrapped_input_function(self):
        out_address = self._memory[self._ip]
        self._memory[out_address] = self._input_function()
        self._ip += 1

    def _get_in_args(self, op, modes):
        n_in = NUM_IN_ARGS[op]
        ins = []
        for i in range(n_in):
            value = self._memory[self._ip]
            if modes[i] == POSITION_MODE:
                ins.append(self._memory[value])
            else:
                ins.append(value)
            self._ip += 1
        return ins

    def _extract_mode_and_operation(self):
        instruction = self._memory[self._ip]
        op = instruction % 100
        c = instruction // 100 % 10
        b = instruction // 1000 % 10
        a = instruction // 10000 % 10
        self._ip += 1
        return op, [c, b, a]

    def _execute_op(self):
        op, modes = self._extract_mode_and_operation()
        args = self._get_in_args(op, modes)
        self._operations[op](*args)

    def run_intcode(self) -> int:
        self._ip = 0
        while self._memory[self._ip] != Instruction.HALT:
            self._execute_op()
        return self._memory[0]

    @property
    def output(self):
        return self._output

import operator


class Instruction:
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    HALT = 99


NUM_IN_ARGS = {
    Instruction.ADD: 2,
    Instruction.MUL: 2,
    Instruction.INPUT: 0,
    Instruction.OUTPUT: 1,
}


POSITION_MODE = 0


class IntCodeComputer:

    def __init__(self, memory: list[int], input_function) -> None:
        self._ip = 0
        self._memory = memory
        self._input_function = input_function
        self._output = []
        self._operations = {
            Instruction.ADD: self._add,
            Instruction.MUL: self._mul,
            Instruction.OUTPUT: self._output_function,
            Instruction.INPUT: self._wrapped_input_function,
        }

    def _add(self, *args):
        out_address = self._memory[self._ip]
        self._memory[out_address] = operator.add(*args)
        self._ip += 1

    def _mul(self, *args):
        out_address = self._memory[self._ip]
        self._memory[out_address] = operator.mul(*args)
        self._ip += 1

    def _output_function(self, arg):
        self._output.append(arg)

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
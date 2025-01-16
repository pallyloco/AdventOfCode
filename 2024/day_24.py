from typing import Optional

from reading import read_paragraphs
import re

input_data = [
    "x00: 1",
    "x01: 0",
    "x02: 1",
    "x03: 1",
    "x04: 0",
    "y00: 1",
    "y01: 1",
    "y02: 1",
    "y03: 1",
    "y04: 1",
    "",
    "ntg XOR fgs -> mjb",
    "y02 OR x01 -> tnw",
    "kwq OR kpj -> z05",
    "x00 OR x03 -> fst",
    "tgd XOR rvg -> z01",
    "vdt OR tnw -> bfw",
    "bfw AND frj -> z10",
    "ffh OR nrd -> bqk",
    "y00 AND y03 -> djm",
    "y03 OR y00 -> psh",
    "bqk OR frj -> z08",
    "tnw OR fst -> frj",
    "gnj AND tgd -> z11",
    "bfw XOR mjb -> z00",
    "x03 OR x00 -> vdt",
    "gnj AND wpb -> z02",
    "x04 AND y00 -> kjc",
    "djm OR pbm -> qhw",
    "nrd AND vdt -> hwm",
    "kjc AND fst -> rvg",
    "y04 OR y02 -> fgs",
    "y01 AND x02 -> pbm",
    "ntg OR kjc -> kwq",
    "psh XOR fgs -> tgd",
    "qhw XOR tgd -> z09",
    "pbm OR djm -> kpj",
    "x03 XOR y03 -> ffh",
    "x00 XOR y04 -> ntg",
    "bfw OR bqk -> z06",
    "nrd XOR fgs -> wpb",
    "frj XOR qhw -> z04",
    "bqk OR frj -> z07",
    "y03 OR x01 -> nrd",
    "hwm AND bqk -> z03",
    "tgd XOR rvg -> z12",
    "tnw OR pbm -> gnj",
]

fh = open("day_24.txt", "r")
input_data = list(map(str.rstrip, fh))

operators = {
    "XOR": lambda r1, r2: r1 ^ r2,
    "AND": lambda r1, r2: r1 & r2,
    "OR": lambda r1, r2: r1 | r2,
}


class Gate:
    def __init__(self, operation: str, input1_str, input2_str, output_str: str):
        self._input1 = None
        self._input2 = None
        self.operation = operation
        self.output_str = output_str
        self.input1_str = input1_str
        self.input2_str = input2_str
        self.output_value = None
        self.name = f"{input1_str}_{input2_str}_{output_str}"

    def output(self) -> Optional[int]:
        if self._input1 is not None and self._input2 is not None:
            self.output_value = operators[self.operation](self._input1, self._input2)
            return self.output_value

    def reset(self):
        self._input1 = None
        self._input2 = None
        self.output_value = None

    @property
    def input1(self):
        return self._input1

    @input1.setter
    def input1(self, value):
        if value != self._input1:
            self._input1 = value
            self.output()

    @property
    def input2(self):
        return self._input2

    @input2.setter
    def input2(self, value):
        if value != self._input2:
            self._input2 = value
            self.output()

    def __str__(self):
        return f"({self.input1_str}:{self._input1},{self.input2_str}:{self._input2} -> {self.output_value}) ({self.output_str})"


def make_graphiz(gates: list[Gate]):
    print("digraph {")
    unique_instructions = set()
    for gate in gates:
        unique_instructions.add(f'{gate.name} [label="{gate.operation}"]')
        if gate.output_str[0] == "z":
            unique_instructions.add(f"{gate.name} -> {gate.output_str}")
        for wire in (gate.input1_str, gate.input2_str):
            for input_gate in (g for g in gates if g.output_str == wire):
                unique_instructions.add(f'{input_gate.name} -> {gate.name} [label={input_gate.output_str}]')
            if wire[0] == "x" or wire[0] == "y" or wire[0] == "C":
                unique_instructions.add(f"{wire} -> {gate.name}")
    for instr in unique_instructions:
        print(instr)
    print("}")


def main(data):
    registers = {}
    pass
    initial, program = read_paragraphs(data)

    gates = []
    for line in initial:
        registers[line[:3]] = int(line[-1])
    for line in program:
        match = re.match(r"(...) (XOR|AND|OR) (...) -> (...)", line)
        r1, op, r2, r3 = match.groups()
        gates.append(Gate(op, r1, r2, r3))
    make_graphiz(gates)

    ans1 = go(gates,registers)
    print(ans1)

    for digit in range(45):

        for nums in ((0, 0), (0, 1,), (1, 0), (1, 1)):
            x = 0
            y = 0
            registers = {a: 0 for a, b in registers.items() if a[0]=="x" or a[0]=="y"}
            for g in gates:
                g.reset()
            registers[f"x{digit:02d}"] = nums[0]
            registers[f"y{digit:02d}"] = nums[1]
            x = nums[0] << digit
            y = nums[1] << digit
            z = go(gates,registers)
            if x+y != z:
                print(f"{digit=}, {x=},{y=}, {x+y=}, {z=}")
                for r in sorted((r for r in registers if r[0] == "z"), reverse=True):
                    print(registers[r],end="")
                print ()

                pass
    ans2_list=["z13","vcv","vwp","z19","z25","mps","cqm","vjv"]
    ans2_list.sort()
    print (",".join(ans2_list))


def go(gates, registers) -> int:
    ans = 0
    while any((g.output_value is None for g in gates)):
        for gate in (g for g in gates if g.output_value is None):
            if gate.input1_str in registers:
                gate.input1 = registers[gate.input1_str]
            if gate.input2_str in registers:
                gate.input2 = registers[gate.input2_str]
            if gate.output_value is not None:
                registers[gate.output_str] = gate.output_value
    for r in sorted((r for r in registers if r[0] == "z"), reverse=True):
        ans = (ans << 1) + registers[r]
    return ans


main(input_data)

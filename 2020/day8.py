
def main():

    file = open('day8_input.txt', 'r')
    data = [str.rstrip(l) for l in file]
    program: Program = Program( data)
    program.run()
    print("Part 1: ", program.accumulator)

    # find a program that does not have an infinite loop by changing only ONE command
    # NOP->jmp or jmp->NOP
    modifiable_addresses = [i for i,op in enumerate(program.code) if op.startswith("jmp") or op.startswith("nop")]
    for address in modifiable_addresses:
        modified_code = [c for c in data]
        opcode, value = modified_code[address].split(" ")
        if opcode == 'nop':
            modified_code[address] = f"jmp {value}"
        elif opcode == 'jmp':
            modified_code[address] = f"nop {value}"
        program: Program = Program( modified_code)
        program.run()
        if not program.is_infinite:
            print("Part 2: ", program.accumulator)
            break

class Program:
    def __init__(self, code):
        self.accumulator: int = 0
        self.program_counter:int = 0
        self.code = code
        self.number_instructions = len(code)
        self.code_coverage: list[int] = [0] * self.number_instructions

    @property
    def is_infinite(self):
        return self.program_counter < self.number_instructions

    def run(self):
        self.accumulator = 0
        self.program_counter = 0
        self.code_coverage: list[int] = [0] * self.number_instructions
        while self.program_counter < self.number_instructions and self.code_coverage[self.program_counter] == 0:
             self.execute_instruction()
        return

    def execute_instruction(self):
        self.code_coverage[self.program_counter] = 1
        opcode, value = self.code[self.program_counter].split(" ")
        if opcode == 'acc':
            self.accumulator += int(value)
            self.program_counter += 1
        elif opcode == 'nop':
            self.program_counter += 1
        elif opcode == 'jmp':
            self.program_counter += int(value)
        return



if __name__ == '__main__':
    main()

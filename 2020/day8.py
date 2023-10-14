"""
You narrow the problem down to a strange infinite loop in the boot code (your puzzle input)
of the device. You should be able to fix it, but first you need to be able to run the code
in isolation.

The boot code is represented as a text file with one instruction per line of text.
Each instruction consists of an operation (acc, jmp, or nop) and
an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in
    the argument. For example, acc +7 would increase the accumulator by 7.
    The accumulator starts at 0. After an acc instruction, the instruction immediately below it
    is executed next.

jmp jumps to a new instruction relative to itself.
    The next instruction to execute is found using the argument as an offset from the jmp instruction;
    for example, jmp +2 would skip the next instruction,
    jmp +1 would continue to the instruction immediately below it,
    and jmp -20 would cause the instruction 20 lines above to be executed next.

nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
"""

accumulator = 0


def main(part: int = 1):
    global accumulator

    file = open('day8_input.txt', 'r')
    program: list[str] = [str.rstrip(l) for l in file]
    code_coverage: list[int] = [0 for i in range(len(program))]

    # start the program at the beginning
    program_counter = 0
    while program_counter < len(program) and code_coverage[program_counter] == 0:
        program_counter = execute(program, program_counter, code_coverage)

    print("Before infinite loop starts, accumulator is", accumulator)

    """
    Fix the program so that it terminates normally by changing 
        exactly one jmp (to nop) 
        or nop (to jmp). 
    What is the value of the accumulator after the program terminates?
    """

    modified_address = -1
    while True:
        if modified_address >= 0:
            _ = switch_opcodes(program, modified_address)

        for i in range(modified_address+1, len(program)):
            if switch_opcodes(program, i):
                modified_address = i
                break

        code_coverage: list[int] = [0 for i in range(len(program))]
        accumulator = 0
        program_counter = 0
        while program_counter < len(program) and code_coverage[program_counter] == 0:
            program_counter = execute(program, program_counter, code_coverage)
        if program_counter == len(program):
            print("After fixing infinite loop, accumulator is", accumulator)
            exit()


def switch_opcodes(program: list[str], index: int) -> bool:
    opcode, value = program[index].split(" ")
    if opcode == 'nop':
        program[index] = f"jmp {value}"
        return True
    elif opcode == 'jmp':
        program[index] = f"nop {value}"
        return True
    return False


def execute(program: list[str], program_counter: int, code_coverage: list[int]) -> int:
    global accumulator
    code_coverage[program_counter] = 1
    opcode, value = program[program_counter].split(" ")
    if opcode == 'acc':
        accumulator += int(value)
        program_counter += 1
    elif opcode == 'nop':
        program_counter += 1
    elif opcode == 'jmp':
        program_counter += int(value)
    #print(opcode, value, "->", program_counter, accumulator)
    return program_counter


if __name__ == '__main__':
    main(1)

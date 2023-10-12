"""
All you need to do is identify the questions for which anyone in your group answers "yes".

For each group, count the number of questions to which anyone answered "yes".

Another group asks for your help, then another, and eventually you've collected answers
from every group on the plane (your puzzle input).

Each group's answers are separated by a blank line, and within each group,
each person's answers are on a single line.

What is the sum of those counts?

For each group, count the number of questions to which everyone answered "yes".
What is the sum of those counts?


"""
from typing import TextIO


def main(part: int = 1):
    total_answered = 0
    file = open('day6_input.txt', 'r')
    total_everyone = 0

    for lines in read_paragraph(file):
        answers: set[str] = set()
        everyone: set[str] = set()

        for i, line in enumerate(lines):
            new_set = set(line)
            answers.update(new_set)
            if i == 0:
                everyone = set(line)
            else:
                everyone.intersection_update(new_set)
        total_answered += len(answers)
        total_everyone += len(everyone)

    print("Total number of answers is:", total_answered)
    print("Total number of everyone is:", total_everyone)


def read_paragraph(file: TextIO) -> list[str]:
    lines: list[str] = list()
    for line in map(str.rstrip, file):
        if line:
            lines.append(line)
        if not line and len(lines) > 0:
            yield lines
            lines.clear()
    yield lines


if __name__ == '__main__':
    main(1)

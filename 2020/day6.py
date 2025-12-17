from reading import read_paragraphs
def main():
    total_answered = 0
    file = open('day6_input.txt', 'r')
    total_everyone = 0

    for lines in read_paragraphs(map(str.strip,file)):
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


if __name__ == '__main__':
    main(1)

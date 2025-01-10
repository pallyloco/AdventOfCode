def read_paragraphs(data) -> list:
    paragraph = []
    for line in data:
        if line == "":
            yield paragraph
            paragraph = []
        else:
            paragraph.append(line)
    yield paragraph

from grid import Grid
data="""..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
data = tuple(map(str.rstrip, data.splitlines()))
fh = open("day_04.txt", "r")
data = tuple(map(str.rstrip, fh.readlines()))

print_room = Grid(data)

def clear_paper(day=1):
    accessible = 0
    while True:
        removed_paper = False
        for paper in print_room:
            number_of_non_empty_neighbours = sum(1 for p in print_room.neighbours(paper) if p is not None)
            if number_of_non_empty_neighbours < 4:
                accessible += 1
                removed_paper = True
                if day != 1:
                    print_room.remove_data_point(paper.row, paper.col)
        if day == 1:
            break
        if not removed_paper:
            break
    return accessible

if __name__ == "__main__":
    print(f"answer 1: {clear_paper(1)}")
    print(f"answer 2: {clear_paper(2)}")




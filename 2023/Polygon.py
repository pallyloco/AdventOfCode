from Grid import Grid
from Coords import Coord
import itertools as it



# ======================================================================================
# Grid carries points that are on the inside edge of the polygon
# ======================================================================================

class Polygon:
    def __init__(self):
        self.points: list[Coord] = list()
        self.grid = Grid()
        self.wall_locations: list[Coord] = list()


    def add_inside_vertex(self, pt: Coord):
        self.grid.set_value(Coord(*pt.row_col(), "#"))
        self.wall_locations.append(pt)

    def outer_vertices(self) -> list[Coord]:
        self._define_vertices(include_edges=True)
        return self.points

    def inner_vertices(self) -> list[Coord]:
        self._define_vertices(include_edges=False)
        return self.points

    def outer_volume(self) -> int:
        if self.wall_locations[0] == self.wall_locations[-1]:
            self.wall_locations.append(self.wall_locations[0])
        p = self.perimeter()
        return self._volume(include_edges=True) + p//2 + 1

    def inner_volume(self) -> int:
        if self.wall_locations[0] == self.wall_locations[-1]:
            self.wall_locations.append(self.wall_locations[0])
        p = self.perimeter()
        return self._volume(include_edges=False) - p//2 + 1


    def perimeter(self) -> int:
        return sum(abs(a.row-b.row+a.col-b.col) for a,b in it.pairwise(self.wall_locations))



    def _volume(self, include_edges=True) -> int:

        total = 0
        for p1,p2 in it.pairwise(self.wall_locations):
            total += (p1.row + p2.row) * (p1.col - p2.col)
        return abs(total // 2)

    def _define_vertices(self, include_edges: bool = True):

        length_of_wall = len(self.wall_locations)
        self.points.clear()

        coords_to_direction: dict[Coord, str] = {
            Coord(1, 0): 'd',
            Coord(-1, 0): 'u',
            Coord(0, 1): 'r',
            Coord(0, -1): 'l'
        }
        min_row = self.grid.min_row()
        min_col = self.grid.min_col()
        max_col = self.grid.max_col()

        # start by finding the lines
        scol = min_col
        for scol in range(min_col, max_col + 1):
            if self.grid.get_data_point(min_row, scol) is not None:
                break

        start = Coord(min_row, scol)

        # where in my list of grid_vertices is the starting position?
        offset = self.wall_locations.index(start)
        next_vertex = self.wall_locations[(offset + 1) % length_of_wall]

        # where do we go from the start? (right or down)
        new_dir = coords_to_direction[start.direction_to(next_vertex)]

        # where is the wall relative to our movement?
        if new_dir == "r":
            dirs = "u"
            if include_edges:
                wall = "right"
            else:
                wall = "left"
        if new_dir == "d":
            dirs = "l"
            if include_edges:
                wall = "below"
            else:
                wall = "above"

        # now loop through the moat and find the outside edge vertices.
        for index in range(len(self.wall_locations)):

            i = (index + offset) % len(self.wall_locations)
            i_plus_1 = (i + 1) % len(self.wall_locations)
            p1 = self.wall_locations[i]
            p2 = self.wall_locations[i_plus_1]
            if p1 == p2:
                continue
            new_dir = coords_to_direction[p1.direction_to(p2)]

            if dirs == 'r':

                # it's a straight line, so we needn't worry process
                if new_dir == "r":
                    continue

                dirs = new_dir
                if dirs == "d" and wall == "below":
                    wall = 'left'
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "d" and wall == "above":
                    wall = "right"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "u" and wall == "below":
                    wall = "right"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "u" and wall == "above":
                    wall = "left"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                else:
                    raise IndexError

            elif dirs == 'l':

                # it's a straight line, so we needn't worry process
                if p1.row == p2.row:
                    continue

                dirs = new_dir
                if dirs == "d" and wall == "below":
                    wall = 'right'
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "d" and wall == "above":
                    wall = "left"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                elif dirs == "u" and wall == "below":
                    wall = "left"
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "u" and wall == "above":
                    wall = "right"
                    self.points.append(Coord(p1.row + 1, p1.col))
                else:
                    raise IndexError

            elif dirs == 'u':

                # it's a straight line, so we needn't worry process
                if p1.col == p2.col:
                    continue

                dirs = new_dir
                if dirs == "r" and wall == "left":
                    wall = 'above'
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                elif dirs == "r" and wall == "right":
                    wall = "below"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "l" and wall == "right":
                    wall = "above"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "l" and wall == "left":
                    wall = "below"
                    self.points.append(Coord(p1.row, p1.col + 1))
                else:
                    raise IndexError

            elif dirs == 'd':

                # it's a straight line, so we needn't worry process
                if p1.col == p2.col:
                    continue

                dirs = new_dir
                if dirs == "r" and wall == "left":
                    wall = 'below'
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "r" and wall == "right":
                    wall = "above"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "l" and wall == "right":
                    wall = "below"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "l" and wall == "left":
                    wall = "above"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                else:
                    raise IndexError
        pass

    def _define_inner_vertices(self):

        coords_to_direction: dict[Coord, str] = {
            Coord(1, 0): 'd',
            Coord(-1, 0): 'u',
            Coord(0, 1): 'r',
            Coord(0, -1): 'l',
            Coord(0, 0): 'x'
        }
        min_row = self.grid.min_row()
        min_col = self.grid.min_col()
        max_col = self.grid.max_col()

        # start by finding the outside of one of the lines
        scol = min_col
        for scol in range(min_col, max_col + 1):
            if self.grid.get_data_point(min_row, scol) is not None:
                break

        start = Coord(min_row, scol)

        # where in my list of grid_vertices is the starting position?
        offset = self.wall_locations.index(start)
        dirs = 'u'
        moat = "right"

        # now loop through the moat and find the outside edge vertices.
        for index in range(len(self.wall_locations)):
            i = (index + offset) % len(self.wall_locations)
            i_plus_1 = (i + 1) % len(self.wall_locations)
            p1 = self.wall_locations[i]
            p2 = self.wall_locations[i_plus_1]
            if p1 == p2:
                continue
            new_dir = coords_to_direction[p1.direction_to(p2)]
            if new_dir == 'x':
                new_dir = {"d": "u", "u": "d", "r": "l", "l": "r"}[dirs]

            if dirs == 'r':

                # it's a straight line, so we needn't worry process
                if new_dir == "r":
                    continue

                dirs = coords_to_direction[p1.direction_to(p2)]
                if dirs == "d" and moat == "below":
                    moat = 'left'
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "d" and moat == "above":
                    moat = "right"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "u" and moat == "below":
                    moat = "right"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "u" and moat == "above":
                    moat = "left"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                else:
                    raise IndexError

            elif dirs == 'l':

                # it's a straight line, so we needn't worry process
                if p1.row == p2.row:
                    continue

                dirs = coords_to_direction[p1.direction_to(p2)]
                if dirs == "d" and moat == "below":
                    moat = 'right'
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "d" and moat == "above":
                    moat = "left"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                elif dirs == "u" and moat == "below":
                    moat = "left"
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "u" and moat == "above":
                    moat = "right"
                    self.points.append(Coord(p1.row + 1, p1.col))
                else:
                    raise IndexError

            elif dirs == 'u':

                # it's a straight line, so we needn't worry process
                if p1.col == p2.col:
                    continue

                dirs = coords_to_direction[p1.direction_to(p2)]
                if dirs == "r" and moat == "left":
                    moat = 'above'
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                elif dirs == "r" and moat == "right":
                    moat = "below"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "l" and moat == "right":
                    moat = "above"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "l" and moat == "left":
                    moat = "below"
                    self.points.append(Coord(p1.row, p1.col + 1))
                else:
                    raise IndexError

            elif dirs == 'd':

                # it's a straight line, so we needn't worry process
                if p1.col == p2.col:
                    continue

                dirs = coords_to_direction[p1.direction_to(p2)]
                if dirs == "r" and moat == "left":
                    moat = 'below'
                    self.points.append(Coord(p1.row, p1.col + 1))
                elif dirs == "r" and moat == "right":
                    moat = "below"
                    self.points.append(Coord(p1.row + 1, p1.col))
                elif dirs == "l" and moat == "right":
                    moat = "above"
                    self.points.append(Coord(p1.row, p1.col))
                elif dirs == "l" and moat == "left":
                    moat = "above"
                    self.points.append(Coord(p1.row + 1, p1.col + 1))
                else:
                    raise IndexError
        pass

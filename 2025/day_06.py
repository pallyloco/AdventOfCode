from dataclasses import dataclass
from functools import reduce
from typing import Callable

data="""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""
data = list(map(str.rstrip,data.splitlines()))
fh = open("day_06.txt", "r")
data = list(map(str.rstrip, fh.readlines()))
operator_line = data.pop()

@dataclass
class ColumnOperator:
    start: int = None
    stop: int = None  # non inclusive (so we can use range)
    value: str = ""
    func: Callable[[str,str],str] = lambda x,y: 0


def cephalopod_math(day = 1):

    # parse
    # - thing to note,
    #   the operator always starts a specific column
    #   AND we need to preserve spaces for part two to work
    column_operators = get_column_info(operator_line, max(map(len,data)))

    # compute
    col_ans = []
    for operator in column_operators:
        col_data = [d for d in column_data_iter(data, operator)]
        if day == 1:
            col_ans.append(int( reduce(operator.func, col_data)))
        else:
            col_ans.append(int(reduce(operator.func, left_right_column(col_data, operator.stop-operator.start))))
    return sum(col_ans)

# using operators ... which always are at the beginning of the columns ... determine all columns
def get_column_info(operator_line, max_len):
    column_operators: list[ColumnOperator] = []

    for i,c in enumerate(operator_line):
        if c != " ":
            if len(column_operators) > 0:
                column_operators[-1].stop = i-1
            co = ColumnOperator(start=i, value=c)
            if c == "+":
                co.func = lambda x,y: str(int(x) + int(y))
            elif c == "*":
                co.func = lambda x,y: str(int(x) * int(y))
            column_operators.append(co)

    if len(column_operators) > 0:
        column_operators[-1].stop = max_len
    return column_operators


def column_data_iter(array: list[str], col:ColumnOperator):
    for r in array:
        yield r[col.start: col.stop]

def left_right_column(col_data: list[str], col_width):
    for i in range(col_width):
        number = 0
        for d in col_data:
            try:
                if d[i] != " ":
                    number = number*10 + int(d[i])
            except IndexError:
                pass
        yield number



if __name__ == "__main__":
    print (f"answer 1: {cephalopod_math(1)}")
    print (f"answer 2: {cephalopod_math(2)}")


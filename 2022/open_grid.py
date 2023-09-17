
import re
# no limits on r,c numbers

class open_grid:
    def __init__ (self):
        self._data = {}
    

    def get_all (self):
        return self._data

    def set_value(self,r,c,value):
        if value is None:
            try:
                del self._data[f"{r},{c}"]
                return
            except KeyError:
                return
        self._data[f"{r},{c}"] = value

    def get_value(self,r,c):
        try:
            return self._data[f'{r},{c}']
        except KeyError:
            return None

    def N(self,r,c):
        return (r-1,c)
    def S(self,r,c):
        return (r+1,c)
    def W(self,r,c):
        return (r,c-1)
    def E(self,r,c):
        return(r,c+1)
    def NE(self,r,c):
        return(r-1,c+1)
    def NW(self,r,c):
        return(r-1,c-1)
    def SE(self,r,c):
        return(r+1,c+1)
    def SW(self,r,c):
        return(r+1,c-1)
    
    def neighbours(self,r,c):
        return (self.N(r,c),self.NE(r,c),self.E(r,c),self.SE(r,c),self.S(r,c),self.SW(r,c),self.W(r,c),self.NW(r,c))

    def get_row_col_pairs(self):
        return ( (int(re.match(r'(-?\d+).*?(-?\d+)',index).group(1)),int(re.match(r'(-?\d+).*?(-?\d+)',index).group(2))) for index in self._data)
    
    def get_row_values(self,row):
        return [self.get_value(row,col) for col in range(self.min_col(),self.max_col()+1)]
    def get_rows(self):
        rows = map(int, ( re.match(r'(-?\d+)',index).group(1) for index in self._data))
        return [*rows]
    def min_row(self):
        r = self.get_rows()
        return min(self.get_rows())
    def max_row(self):
        return max(self.get_rows())
    def num_rows(self):
        return self.max_row - self.min_row + 1

    def get_col_values(self,col):
        return [self.get_value(row,col) for row in range(self.min_row,self.max_row+1)]
    def get_cols(self):
        cols = map(int, ( re.match(r'(-?\d+).*?(-?\d+)',index).group(2) for index in self._data))
        return [*cols]
    def min_col(self):
        a=self.get_cols()
        return min(self.get_cols())
    def max_col(self):
        return max(self.get_cols())
    def num_cols(self):
        return self.max_col - self.min_col + 1
    
    def empty(self):
        total = 0
        for row in range(self.min_row(),self.max_row()+1):
            s=sum ( (1 for value in self.get_row_values(row) if value is None) )
            total += s
        return total

    def __str__(self):
        str = ""
        for r in range(self.min_row(),self.max_row()+1):
            for c in range(self.min_col(),self.max_col()+1):
                if self.get_value(r,c) is None:
                    str += "."
                else:
                    str += "#"
            str+="\n"
        return str

    def __repr__(self):
        return self.__str__()


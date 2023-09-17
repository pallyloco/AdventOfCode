
class DynamicGrid:
    def __init__ (self):
        self._data = [ [None] ]
    

    def get_all (self):
        return self._data

    def add(self,r,c,data):
        try:
            self._data[r][c] = data
        except IndexError:
            self._data = self._data + [[None] for i in range(r-len(self._data)+1)]
            self._data[r] = self._data[r] + [None for i in range(c - len(self._data[r])+1)]
            self._data[r][c] = data
    
    def get(self,r,c):
        try:
            return self._data[ r ][c]
        except IndexError:
            return None
    
    def num_rows(self):
        return len(self._data) 

    def children(self,r,c):
        coords = []
        for rc in range(-1,  1 ):
            for cc in range(-1, 1):
                if rc != r or cc != c:
                    coords.append( self.get(rc, cc) ) 
        return coords

    def ordinal_children(self,r,c):
        coords = self.children(r,c)
        ord_coords = [coord for coord in coords if coord.r == r or coord.c == c]
        return ord_coords

    def __str__(self):
        str = ""
        for r in range(self.num_rows()):
            str+=f"{self._data[r]}\n"
        return str

    def __repr__(self):
        return self.__str__()



class Grid:
    def __init__ (self, width):
        self.width = width
        self._data = []
    

    def get_all (self):
        return self._data

    def add(self,r,c,data):
        
        if c >= self.width:
            raise Exception("Invalid indices")

        try:
            self._data[ r * self.width + c ] = DataPoint(r,c,data,self)
        except IndexError:
            self._data += [None]*self.width
            self.add(r,c,data)
    
    def get(self,r,c):
        try:
            return self._data[ r * self.width + c]
        except IndexError:
            return None
    
    def num_rows(self):
        return len(self._data) // self.width

    def children(self,r,c):
        coords = []
        rmin = max(0,r-1)
        rmax = min(r+1,self.num_rows()-1)
        cmin = max(0,c-1)
        cmax = min(c+1,self.width-1)
        for rc in range(rmin, rmax + 1 ):
            for cc in range(cmin,cmax + 1):
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
            str +=  f"{[self.get(r,c) for c in range(self.width)]}\n"
        return str

    def __repr__(self):
        return self.__str__()

class DataPoint:
    def __init__(self,r,c,value,map):
        self.r = r
        self.c = c
        self.value = value
    
    def __str__(self):
        return f"{self.value}"
    
    def __repr__(self):
        return self.__str__()
    
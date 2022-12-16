
class DictionaryGrid:
    def __init__ (self):
        self._data = dict()
        self.max_row = None
        self.min_row = None
        self.max_col = None
        self.min_col = None
    

    def get_all (self):
        return self._data.values

    def add(self,r,c,data):
        self._data[f"{r,c}"] = data
        self.max_row = r if self.max_row is None else max(r,self.max_row)
        self.min_row = r if self.min_row is None else min(r,self.min_row)
        self.max_col = c if self.max_col is None else max(c,self.max_col)
        self.min_col = c if self.min_col is None else min(c,self.min_col)
    
    def get(self,r,c):
        try:
            return self._data[ f"{r,c}"]
        except KeyError:
            return None
    
    def num_rows(self):
        return len(self._data) 



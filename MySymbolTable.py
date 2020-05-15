class SymbolTable:
    def __init__(self):
        self.symbol_list = []
        self.location_list = []
        self.extdef_list = []
        self.extref_list = []

    def put_symbol(self, symbol, location, index):
        self.symbol_list.insert(index, symbol)
        self.location_list.insert(index, location)
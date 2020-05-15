class SymbolTable:
    def __init__(self):
        self.symbol_list = []
        self.location_list = []
        self.extdef_list = []
        self.extref_list = []

    def put_symbol(self, symbol, location):
        self.symbol_list.append(symbol)
        self.location_list.append(location)

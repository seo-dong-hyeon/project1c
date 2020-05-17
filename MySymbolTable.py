class SymbolTable:
    def __init__(self):
        self.symbol_list = []
        self.location_list = []
        self.extdef_list = []
        self.extref_list = []

    def put_symbol(self, symbol, location):
        self.symbol_list.append(symbol)
        self.location_list.append(location)

    def search(self, symbol):
        address = -1

        symbol = symbol.rstrip("\n")
        if (symbol.find("#") != -1):
            symbol = symbol.replace("#", "")
        if (symbol.find("@") != -1):
            symbol = symbol.replace("@", "")

        for i, value in enumerate(self.symbol_list):
            if(value.find(symbol) != -1):
                address = self.location_list[i]
                break

        return address




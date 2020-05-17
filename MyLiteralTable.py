class LiteralTable:
    def __init__(self):
        self.literal_list = []
        self.location_list = []
        self.tmp_list = []

    def put_literal(self, literal, location):
        self.literal_list.append(literal)
        self.location_list.append(location)

    def search(self, literal):
        address = -1

        literal = literal.rstrip("\n")
        if (literal.find("#") != -1):
            literal = literal.replace("#", "")
        if (literal.find("@") != -1):
            literal = literal.replace("@", "")

        for i, value in enumerate(self.literal_list):
            if(value.find(literal) != -1):
                address = self.location_list[i]
                break

        return address
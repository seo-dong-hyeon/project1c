class LiteralTable:
    def __init__(self):
        self.literal_list = []
        self.location_list = []
        self.tmp_list = []

    def put_literal(self, literal, location):
        self.literal_list.append(literal)
        self.location_list.append(location)
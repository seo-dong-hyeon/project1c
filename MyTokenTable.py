class TokenTable:
    MAX_OPERAND = 3
    nFlag = 32
    iFlag = 16
    xFlag = 8
    bFlag = 4
    pFlag = 2
    eFlag = 1

    def __init__(self, symTab, instTab):
        self.symTab = symTab
        self.instTab = instTab
        self.token_list = []
        self.program_length = 0

class Token:
    def __init__(self, line):
        self.nixbpe = 0X00
        self.object_code = ""
        self.operand = []

        self.label = ""
        self.operator = ""
        self.operand.insert(0, "")
        self.comment = ""

        self.parsing(self, line)

    def parsing(self, line):
        parsed_line = line.split("\t")

        if(parsed_line[0] == '.'):
            return

        for index, value in enumerate(parsed_line):
            if index == 0:
                self.label += parsed_line[index]
            if index == 1:
                self.operator += parsed_line[index]
            if index == 2:
                self.operand.insert(0, parsed_line[index])
            if index == 3:
                self.comment += parsed_line[index]

        return

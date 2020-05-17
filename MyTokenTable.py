class TokenTable:
    MAX_OPERAND = 3
    nFlag = 32
    iFlag = 16
    xFlag = 8
    bFlag = 4
    pFlag = 2
    eFlag = 1

    def __init__(self, symTab, instTab, literalTab):
        self.symTab = symTab
        self.instTab = instTab
        self.literalTab = literalTab
        self.token_list = []
        self.program_length = 0

    def put_token(self, line):
        token = Token(line)
        self.token_list.append(token)

    def get_token(self, token_index):
        return self.token_list[token_index]

    def make_object_code(self, token_index):
        object_code = ""
        token = self.get_token(token_index)

        if token.operator.find("+") != -1:
            operator = token.operator.replace("+", "")
            opcode = self.instTab.get_opcode(operator)
            object_code += opcode[0]
            if token.operand[0].find(",") != -1:
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 1)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 1)
            else:
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 1)
            object_code += self.make_object_code_second_and_third(token_index, opcode)
            object_code += "00000"
        elif self.instTab.get_format(token.operator) == "3/4":
            opcode = self.instTab.get_opcode(token.operator)
            object_code += opcode[0]
            if token.operand[0] == "":
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 1)
                token.set_flag(TokenTable.eFlag, 0)
                object_code += self.make_object_code_second_and_third(token_index, opcode)
            elif token.operand[0].find("#") != -1:
                token.set_flag(TokenTable.nFlag, 0)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 0)
                object_code += self.make_object_code_second_and_third(token_index, opcode)

                operand = token.operand[0].replace("#", "")
                disp = str(hex(int(operand)).upper().replace("0X", ""))
                if len(disp) == 2:
                    object_code += "0"
                elif len(disp) == 1:
                    object_code += "00"
                object_code += disp
            else:
                if token.operand[0].find("@") != -1:
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 0)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.symTab.search(token.operand[0])
                elif token.operand[0].find("=") != -1:
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 1)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.literalTab.search(token.operand[0])
                else:
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 1)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.symTab.search(token.operand[0])

                object_code += self.make_object_code_second_and_third(token_index, opcode)
                target_address = pc - (token.locctr + 3)
                disp = target_address & 0xFFF
                rest = str(hex(disp)).upper().replace("0X","")

                if len(rest) == 2:
                    object_code += "0"
                elif len(rest) == 1:
                    object_code += "00"
                object_code += rest
        else:
            opcode = self.instTab.get_opcode(token.operator)
            object_code += opcode

            register = token.operand[0].split(",")
            if register[0] == "X":
                object_code += "1"
            elif register[0] == "A":
                object_code += "0"
            elif register[0] == "S":
                object_code += "4"
            elif register[0] == "T":
                object_code += "5"

            if token.operand[0].find(",") != -1:
                if register[1] == "X":
                    object_code += "1"
                elif register[1] == "A":
                    object_code += "0"
                elif register[1] == "S":
                    object_code += "4"
                elif register[1] == "T":
                    object_code += "5"
            else:
                object_code += "0"

        return object_code

    def make_object_code_second_and_third(self, index, opcode):
        object_code_second_and_third = ""
        ni = 0
        if self.get_token(index).get_flag(TokenTable.nFlag) != 0:
            ni += 2
        if self.get_token(index).get_flag(TokenTable.iFlag) != 0:
            ni += 1

        if opcode[1] >= '0' and opcode[1] <= '9':
            ni += int(opcode[1])
            object_code_second_and_third += str(hex(ni)).upper().replace("0X","")
        else:
            ni += int(opcode[1], 16)
            object_code_second_and_third += str(hex(ni)).upper().replace("0X","")

        if self.get_token(index).operand[0] == "":
            object_code_second_and_third += "0000"
            return object_code_second_and_third

        xbpe = 0
        if self.get_token(index).get_flag(TokenTable.xFlag) != 0:
            xbpe += TokenTable.xFlag
        if self.get_token(index).get_flag(TokenTable.bFlag) != 0:
            xbpe += TokenTable.bFlag
        if self.get_token(index).get_flag(TokenTable.pFlag) != 0:
            xbpe += TokenTable.pFlag
        if self.get_token(index).get_flag(TokenTable.eFlag) != 0:
            xbpe += TokenTable.eFlag
        object_code_second_and_third += str(hex(xbpe)).upper().replace("0X","")

        return object_code_second_and_third

class Token:
    def __init__(self, line):
        self.nixbpe = 0X00
        self.object_code = ""
        self.operand = []

        self.label = ""
        self.operator = ""
        self.operand.append("")
        self.comment = ""

        self.parsing(line)

    def parsing(self, line):
        parsed_line = line.split("\t")

        if parsed_line[0] == '.':
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

    def set_flag(self, flag, value):
        if value == 1:
            self.nixbpe = self.nixbpe | flag

    def get_flag(self, flags):
        return self.nixbpe & flags

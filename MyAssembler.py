from MyInstTable import InstTable
from MySymbolTable import SymbolTable
from MyLiteralTable import LiteralTable
from MyTokenTable import TokenTable
from MyTokenTable import Token

class Assembler:
    def __init__(self):
        # self.* : 인스턴스변수
        self.inst_table = InstTable("inst.data")
        self.inst_table.open_file()
        self.line_list = []
        self.symtab_list = []
        self.literal_list = []
        self.Token_list = []
        self.code_list = []

        self.section = 0;
        self.token_index = 0;
        self.locctr = 0;

    def load_input_file(self, input_file):
        f = open(input_file, 'r')
        lines = f.readlines()
        for line in lines:
            self.line_list.append(line)
        f.close()

    def pass1(self):
        program_cnt = 3
        i = 0

        while i < program_cnt:
            symbol_table = SymbolTable()
            self.symtab_list.append(symbol_table)
            literal_table = LiteralTable()
            self.literal_list.append(literal_table)
            token_table = TokenTable(self.symtab_list[i], self.inst_table, self.literal_list[i])
            self.Token_list.append(token_table)
            i += 1

        for index, value in enumerate(self.line_list):
            token = Token(value)
            token.operator = token.operator.rstrip("\n")

            if token.operator == "":
                continue
            if token.operator == "START":
                self.locctr = 0
                self.token_index = 0
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "CSECT":
                self.locctr = 0
                self.token_index = 0
                self.section += 1
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "RESW":
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
                self.locctr += int(token.operand[0]) * 3
            elif token.operator == "RESB":
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
                self.locctr += int(token.operand[0])
            elif token.operator == "WORD":
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
                self.locctr += 3
            elif token.operator == "BYTE":
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1

                if token.operand[0][0] == "C":
                    self.locctr += len(token.operand[0]) - 3
                elif token.operand[0][0] == "X":
                    self.locctr += int((len(token.operand[0]) - 3) / 2)
            elif token.operator == "EXTDEF":
                self.Token_list[self.section].symTab.put_extdef(token.operand[0])
            elif token.operator == "EXTREF":
                self.Token_list[self.section].symTab.put_extdef(token.operand[0])
            elif token.operator == "END":
                continue
            elif token.operator == "EQU":
                if token.operand[0].find("*") == -1:
                    parsed_operand = token.operand[0].split("-")
                    self.locctr = self.Token_list[self.section].symTab.search(parsed_operand[0]) - \
                                  self.Token_list[self.section].symTab.search(parsed_operand[1])
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "LTORG":
                self.make_literaltab()
                self.token_index += 1
            else:
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1

                if token.operator[0] == "+":
                    self.locctr += 4
                elif self.inst_table.get_format(token.operator) == "3/4":
                    self.locctr += 3
                else:
                    self.locctr += 2

                if token.operand[0].find('=') != -1:
                    is_present = False
                    for literal_index, literal in enumerate(self.Token_list[self.section].literalTab.tmp_list):
                        if literal == token.operand[0]:
                            is_present = True
                            break
                    if is_present is not True:
                        self.Token_list[self.section].literalTab.tmp_list.append(token.operand[0])

            if self.locctr > self.Token_list[self.section].program_length:
                self.Token_list[self.section].program_length = self.locctr

        self.make_literaltab()
        if self.locctr > self.Token_list[self.section].program_length:
            self.Token_list[self.section].program_length = self.locctr

        '''i = 0
        while i <= self.section:
            for index, value in enumerate(self.Token_list[i].token_list):
                print(str(hex(self.Token_list[i].get_token(index).locctr)) +" "+value.label +" "+value.operator +" "+ value.operand[0])
            i += 1'''

    def make_symtab(self):
        self.Token_list[self.section].get_token(self.token_index).locctr = self.locctr
        token = self.Token_list[self.section].get_token(self.token_index)

        if token.label == "":
            return

        self.Token_list[self.section].symTab.put_symbol(token.label, self.locctr)

    def make_literaltab(self):
        for index, value in enumerate(self.Token_list[self.section].literalTab.tmp_list):
            line = "\tLTORG\t"+ value

            self.Token_list[self.section].put_token(line)
            self.Token_list[self.section].get_token(self.token_index).locctr = self.locctr
            self.Token_list[self.section].literalTab.put_literal(value, self.locctr)

            if value[1] == 'C':
                self.locctr += len(value) - 4
            elif value[1] == 'X':
            	self.locctr += (len(value) - 4) / 2

        self.Token_list[self.section].literalTab.tmp_list.clear()

    def print_symbol_table(self, file_name):
        f = open(file_name, 'w')
        i = 0

        while i <= self.section:
            for index, value in enumerate(self.Token_list[i].symTab.symbol_list):
                location_counter = str(hex(self.Token_list[i].symTab.location_list[index])).upper()
                f.write(value +"\t"+ location_counter[2:] +"\n")
            f.write("\n")
            i += 1
        f.close()

    def print_literal_table(self, file_name):
        f = open(file_name, 'w')
        i = 0

        while i <= self.section:
            for index, value in enumerate(self.Token_list[i].literalTab.literal_list):
                value = value.replace("=C","")
                value = value.replace("=X","")
                value = value.replace("'", "")
                location_counter = str(hex(self.Token_list[i].literalTab.location_list[index])).upper()
                f.write(value +"\t"+ location_counter[2:] +"\n")
            i += 1
        f.close()

    def pass2(self):
        for i, token_table in enumerate(self.Token_list):
            for j, token in enumerate(token_table.token_list):
                token.operator = token.operator.rstrip("\n")
                if token.operator == "START" or token.operator == "CSECT":
                    self.code_list.append("")
                    continue
                elif token.operator == "RESW" or token.operator == "RESB":
                    self.code_list.append("")
                    continue
                elif (token.operator == "EXTDEF" or token.operator == "EXTREF" or token.operator == "END"
                      or token.operator == "EQU"):
                    self.code_list.append("")
                    continue
                elif token.operator == "WORD":
                    token.object_code += "000000"
                    self.code_list.append(token.object_code)
                elif token.operator == "BYTE":
                    object_code = token.operand[0].replace("=C","")
                    object_code = object_code.replace("=X","")
                    object_code = object_code.replace("'","")

                    token.object_code += object_code
                    self.code_list.append(token.object_code)
                elif token.operator == "LTORG":
                    literal = token.operand[0].replace("=", "")
                    literal = literal.replace("'", "")

                    if literal.find("C") != -1:
                        literal = literal.replace("C", "")
                        for k in range(len(literal)):
                            token.object_code += str(ord(literal[k])).upper()
                    elif literal.find("X") != -1:
                        literal = literal.replace("X", "")
                        for k in range(len(literal)):
                            token.object_code += str(literal[k]).upper()
                    self.code_list.append(token.object_code)
                else:
                    token.object_code += token_table.make_object_code(j)
                    self.code_list.append(token.object_code)

        for i, value in enumerate(self.code_list):
            print(value)





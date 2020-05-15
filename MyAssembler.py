from MyInstTable import InstTable
from MySymbolTable import SymbolTable
from MyLiteralTable import LiteralTable
from MyTokenTable import TokenTable
from MyTokenTable import Token

class Assembler:
    def __init__(self):
        # self.* : 인스턴스변수
        self.inst_table = InstTable
        self.inst_table.__init__(self.inst_table, "inst.data")
        self.line_list = []
        self.symtab_list = []
        self.literal_list = []
        self.Token_list = []
        self.code_list = []

        self.section = 0;
        self.token_index = 0;
        self.symbol_index = 0;
        self.locctr = 0;

        #print(self.inst_table.get_opcode(self.inst_table, 'WD'))

    def load_input_file(self, input_file):
        f = open(input_file, 'r')
        lines = f.readlines()
        i = 0
        for line in lines:
            self.line_list.insert(i, line)
            i += 1
        f.close()

        #for index, value in enumerate(self.line_list):
            #print(index, value)

    def pass1(self):
        program_cnt = 3
        i = 0

        while i < program_cnt:
            symbol_table = SymbolTable
            symbol_table.__init__(symbol_table)
            self.symtab_list.insert(i, symbol_table)

            literal_table = LiteralTable
            literal_table.__init__(literal_table)
            self.literal_list.insert(i, literal_table)

            token_table = TokenTable
            token_table.__init__(token_table, self.symtab_list[i], self.inst_table)
            self.Token_list.insert(i, token_table)

            i += 1

        for index, value in enumerate(self.line_list):
            token = Token
            token.__init__(token, value)
            token.operator = token.operator.rstrip("\n")

            if(token.operator == ""):
                continue

            if(token.operator == "START"):
                self.locctr = 0
                self.token_index = 0

                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                #print(self.Token_list[section].get_token(self.Token_list[section], self.token_index).operator)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1
            elif(token.operator == "CSECT"):
                self.locctr = 0
                self.token_index = 0
                self.section += 1

                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1
            elif(token.operator == "RESW"):
                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1

                self.locctr += int(token.operand[0]) * 3
            elif (token.operator == "RESB"):
                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1

                self.locctr += int(token.operand[0])
            elif (token.operator == "WORD"):
                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1

                self.locctr += 3
            elif (token.operator == "BYTE"):
                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1

                if(token.operand[0][0] == "C"):
                    self.locctr += len(token.operand[0]) - 3
                elif(token.operand[0][0] == "X"):
                    self.locctr += int((len(token.operand[0]) - 3) / 2)
            elif (token.operator == "EXTDEF"):
                continue
            elif (token.operator == "EXTREF"):
                continue
            elif (token.operator == "END"):
                continue
            elif (token.operator == "EQU"):
                continue
            elif (token.operator == "LTORG"):
                continue
            else:
                self.Token_list[self.section].put_token(self.Token_list[self.section], value, self.token_index)
                self.make_symtab(self)
                self.token_index += 1
                self.symbol_index += 1

                if(token.operator[0] == "+"):
                    self.locctr += 4
                elif (self.inst_table.get_format(self.inst_table, token.operator) == "3/4"):
                    self.locctr += 3
                else:
                    self.locctr += 2

            '''value = value.rstrip("\n")
            location_counter = self.Token_list[self.section].get_token(self.Token_list[self.section], self.token_index-1).locctr
            h = hex(location_counter)
            print(value +"\t"+ str(h))'''


    def make_symtab(self):
        self.Token_list[self.section].get_token(self.Token_list[self.section], self.token_index).locctr = self.locctr
        token = self.Token_list[self.section].get_token(self.Token_list[self.section], self.token_index)

        if(token.label == ""):
            return;

        self.Token_list[self.section].symTab\
            .put_symbol(self.Token_list[self.section].symTab, token.label, self.locctr, self.symbol_index)







        




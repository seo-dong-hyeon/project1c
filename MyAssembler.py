from MyInstTable import InstTable
from MySymbolTable import SymbolTable
from MyLiteralTable import LiteralTable
from MyTokenTable import TokenTable
from MyTokenTable import Token

class Assembler:
    section = 0;
    token_index = 0;
    locctr = 0;

    def __init__(self):
        # self.* : 인스턴스변수
        self.inst_table = InstTable
        self.inst_table.__init__(self.inst_table, "inst.data")
        self.line_list = []
        self.symtab_list = []
        self.literal_list = []
        self.token_list = []
        self.code_list = []

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
            self.token_list.insert(i, token_table)

            i += 1

        for index, value in enumerate(self.line_list):
            token = Token
            token.__init__(token, value)
            print(token.operator)




        




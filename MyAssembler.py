from MyInstTable import InstTable
from MySymbolTable import SymbolTable
from MyLiteralTable import LiteralTable
from MyTokenTable import TokenTable
from MyTokenTable import Token

class Assembler:
    def __init__(self):
        self.inst_table = InstTable("inst.data") # instruction 명세를 저장한 공간
        self.line_list = [] # 읽어들인 input 파일의 내용을 한 줄 씩 저장하는 공간
        self.symtab_list = [] # 프로그램의 section별로 symbol table을 저장하는 공간
        self.literal_list = [] # 프로그램의 section별로 literal table을 저장하는 공간
        self.Token_list = [] # 프로그램의 section별로 프로그램을 저장하는 공간
        self.code_list = [] # 만들어진 오브젝트 코드들을 출력 형태로 저장하는 공간

        self.section = 0 # 현재 프로그램의 상태를 나타내는 변수(0->COPY프로그램, 1->RDREC프로그램, 2->WDREC프로그램)
        self.token_index = 0 # token_list에 몇개의 토큰이 저장되어 있는지를 나타냄
        self.locctr = 0 # location counter를 저장한 변수

    '''파일의 내용을 한 줄씩 읽어 line_list에 저장'''
    def load_input_file(self, input_file):
        f = open(input_file, 'r')
        lines = f.readlines()
        for line in lines:
            self.line_list.append(line)
        f.close()

    '''프로그램 소스를 스캔하여 토큰단위로 분리한 뒤 토큰테이블 생성'''
    def pass1(self):
        program_cnt = 3 # program의 개수
        i = 0

        '''table 생성 및 초기화'''
        while i < program_cnt:
            # symbol table 생성
            symbol_table = SymbolTable()
            self.symtab_list.append(symbol_table)
            # literal table 생성
            literal_table = LiteralTable()
            self.literal_list.append(literal_table)
            # token table table 생성
            token_table = TokenTable(self.symtab_list[i], self.inst_table, self.literal_list[i])
            self.Token_list.append(token_table)
            i += 1

        '''토큰 분석 시작'''
        for index, value in enumerate(self.line_list):
            token = Token(value) # input 파일의 매 라인을 분석하여 토큰에 저장
            token.operator = token.operator.rstrip("\n") # 명령어의 개행 제거
            if token.operator == "": # 주석이면 넘어감
                continue
            if token.operator == "START": #operator가 START면
                '''변수 초기화'''
                self.locctr = 0
                self.token_index = 0
                self.Token_list[self.section].put_token(value) # 해당 section에 토큰을 삽입
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "CSECT": #operator가 CSECT면
                self.locctr = 0
                self.token_index = 0
                self.section += 1 # 다음 프로그램으로 넘어갔으므로 section을 증가
                self.Token_list[self.section].put_token(value)
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "RESW": #operator가 RESW면
                self.Token_list[self.section].put_token(value)
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
                self.locctr += int(token.operand[0]) * 3 #operand의 길이에 3을 곱한 값을 더하여 다음 location counter 계산
            elif token.operator == "RESB": #operator가 RESB면
                self.Token_list[self.section].put_token(value)
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
                self.locctr += int(token.operand[0]) #operand의 길이를 더하여 다음 location counter 계산
            elif token.operator == "WORD": #operator가 WORD면
                self.Token_list[self.section].put_token(value)
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
                self.locctr += 3 # 1 WORD이므로 3바이트를 더하여 다음 location counter 계산
            elif token.operator == "BYTE": #operator가 BYTE면
                self.Token_list[self.section].put_token(value)
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_symtab()
                self.token_index += 1
                '''C 타입이면 '=', '문자를 뺀 나머지 길이를 더하여  다음 location counter 계산'''
                '''X 타입이면 '=','문자를 뺀 나머지 길이이 절반을 더하여  다음 location counter 계산'''
                if token.operand[0][0] == "C":
                    self.locctr += len(token.operand[0]) - 3
                elif token.operand[0][0] == "X":
                    self.locctr += int((len(token.operand[0]) - 3) / 2)
            elif token.operator == "EXTDEF": #외부 변수 저장
                self.Token_list[self.section].symTab.put_extdef(token.operand[0])
            elif token.operator == "EXTREF": #외부 변수 저장
                self.Token_list[self.section].symTab.put_extref(token.operand[0])
            elif token.operator == "END":
                continue
            elif token.operator == "EQU": #operator가 EQU면
                if token.operand[0].find("*") == -1: # operand가 현재 주소를 나타내는 *가 아니면
                    parsed_operand = token.operand[0].split("-") #'-'문자를 기준으로 앞, 뒤 operand를 나누고
                    # search함수로 각각의 location counter 값을 찾은 뒤 빼줌
                    self.locctr = self.Token_list[self.section].symTab.search(parsed_operand[0]) - \
                                  self.Token_list[self.section].symTab.search(parsed_operand[1])
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1
            elif token.operator == "LTORG": #operator가 LTOGR면
                '''literal table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.make_literaltab()
                self.token_index += 1
            else: #그 외 operator
                '''symbol table 생성 작업 및 토큰 추가로 인한 인덱스 증가'''
                self.Token_list[self.section].put_token(value)
                self.make_symtab()
                self.token_index += 1

                '''format에 따라 다음 location counter값을 다르게 계산'''
                if token.operator[0] == "+":
                    self.locctr += 4
                elif self.inst_table.get_format(token.operator) == "3/4":
                    self.locctr += 3
                else:
                    self.locctr += 2

                if token.operand[0].find('=') != -1: #operand가 literal이면
                    is_present = False
                    '''이미 존재하는 literal인지 확인하고'''
                    for literal_index, literal in enumerate(self.Token_list[self.section].literalTab.tmp_list):
                        if literal == token.operand[0]:
                            is_present = True
                            break
                    '''존재하지 않는 literal이면 임시 literal list에 삽입'''
                    if is_present is not True:
                        self.Token_list[self.section].literalTab.tmp_list.append(token.operand[0])
            '''각 프로그램의 최종 location counter를 program 길이를 나타내는 변수에 저장'''
            if self.locctr > self.Token_list[self.section].program_length:
                self.Token_list[self.section].program_length = self.locctr

        '''프로그램 종료 후에도 LTORG가 나오지 않아'''
        '''location counter가 할당되지 않는 literal에 location counter 할당'''
        self.make_literaltab()
        if self.locctr > self.Token_list[self.section].program_length:
            self.Token_list[self.section].program_length = self.locctr

    '''추가한 함수'''
    '''symbol table을 생성하는 함수'''
    '''반복적 작업의 코드를 줄이고자 모듈화'''
    def make_symtab(self):
        self.Token_list[self.section].get_token(self.token_index).locctr = self.locctr
        token = self.Token_list[self.section].get_token(self.token_index)

        if token.label == "": #label이 없다면 넘어감
            return

        #label과 location counter를 매칭하여 저장
        self.Token_list[self.section].symTab.put_symbol(token.label, self.locctr)

    '''추가한 함수'''
    '''literal table을 생성하는 함수'''
    '''반복적 작업의 코드를 줄이고자 모듈화'''
    def make_literaltab(self):
        for index, value in enumerate(self.Token_list[self.section].literalTab.tmp_list):
            line = "\tLTORG\t"+ value

            '''임시로 literal들을 저장해두었던 list 멤버들을 literal table에 옮김'''
            '''operand의 타입에 따라 다르게 다음 location counter값을 계산'''
            '''operator를 LTORG로 operand를 literal list의 첫번쨰 원소로 구성하여 토큰에 저장'''
            self.Token_list[self.section].put_token(line)
            self.Token_list[self.section].get_token(self.token_index).locctr = self.locctr
            self.Token_list[self.section].literalTab.put_literal(value, self.locctr)

            '''임시로 literal들을 저장해두었던 list 멤버들을 실제 literal table에 옮기는 작업'''
            if value[1] == 'C': # C타입이면 '=','C','''문자를 제외한 문자열 길이만큼을 locctr에 더함
                self.locctr += len(value) - 4
            elif value[1] == 'X': # X타입이면 '=','X','''문자를 제외한 문자열 길이의 절반만큼을 locctr에 더함
            	self.locctr += (len(value) - 4) / 2

        #임시로 literal들을 저장해두었던 list 멤버들을 literal table에 옮겼으므로 초기화
        self.Token_list[self.section].literalTab.tmp_list.clear()

    '''작성된 SymbolTable들을 출력형태에 맞게 출력'''
    def print_symbol_table(self, file_name):
        f = open(file_name, 'w')
        i = 0

        '''TokenList의 size = 프로그램의 개수만큼 진행'''
        while i <= self.section:
            '''TokenList의 각각의 프로그램의 symbol list 길이만큼 진행'''
            for index, value in enumerate(self.Token_list[i].symTab.symbol_list):
                '''symbol list의 원소인 symbol과 location counter 값을 묶어서 문자열로 만듦'''
                location_counter = str(hex(self.Token_list[i].symTab.location_list[index])).upper()
                f.write(value +"\t"+ location_counter[2:] +"\n")
            f.write("\n") #각각의 프로그램이 끝날때마다 개행
            i += 1
        f.close()

    '''작성된 LiteralTable들을 출력형태에 맞게 출력'''
    def print_literal_table(self, file_name):
        f = open(file_name, 'w')
        i = 0

        '''TokenList의 size = 프로그램의 개수만큼 진행'''
        while i <= self.section:
            '''TokenList의 각각의 프로그램의 literal list 길이만큼 진행'''
            for index, value in enumerate(self.Token_list[i].literalTab.literal_list):
                '''literal list의 원소인 literal과 location counter을 묶어서 문자열로 만듦'''
                '''literal 파일에 저장전 '=','C','X',' 등의 문자는 제외함'''
                value = value.replace("=C","")
                value = value.replace("=X","")
                value = value.replace("'", "")
                location_counter = str(hex(self.Token_list[i].literalTab.location_list[index])).upper()
                f.write(value +"\t"+ location_counter[2:] +"\n")
            i += 1
        f.close()

    '''분석된 내용을 바탕으로 object code를 생성하여 codeList에 저장'''
    def pass2(self):
        '''TokenList의 size = 프로그램의 개수만큼 진행'''
        for i, token_table in enumerate(self.Token_list):
            '''TokenList의 각각의 프로그램의 token list의 길이만큼 진행'''
            for j, token in enumerate(token_table.token_list):
                token.operator = token.operator.rstrip("\n")
                '''operator가 특정 지시어일땐 object code를 생성하지 않고 넘어감'''
                if token.operator == "START" or token.operator == "CSECT":
                    continue
                elif token.operator == "RESW" or token.operator == "RESB":
                    continue
                elif (token.operator == "EXTDEF" or token.operator == "EXTREF" or token.operator == "END"
                      or token.operator == "EQU"):
                    continue
                elif token.operator == "WORD": #operator가 WORD면
                    token.object_code += "000000" #주소를 알 수 없으므로 6자리 object code를 모두 0으로
                    self.code_list.append(token.object_code)
                elif token.operator == "BYTE": #operator가 BYTE면
                    '''operand에서 'X','C','문자를 제외하여 object code에 그대로 저장'''
                    object_code = token.operand[0].replace("=C","")
                    object_code = object_code.replace("=X","")
                    object_code = object_code.replace("'","")
                    token.object_code += object_code
                    self.code_list.append(token.object_code)
                elif token.operator == "LTORG": #operator가 LTOGR면
                    '''operand를 literal 변수에 저장 후 '=', '문자를 지움'''
                    literal = token.operand[0].replace("=", "")
                    literal = literal.replace("'", "")

                    '''literal이 C타입이면'''
                    if literal.find("C") != -1:
                        ''''C'문자를 지우고 literal의 각 문자를 16진수로 변환후 objectCode에 그대로 저장'''
                        literal = literal.replace("C", "")
                        for k in range(len(literal)):
                            token.object_code += str(hex(ord(literal[k]))).upper().replace("0X", "")
                    elif literal.find("X") != -1: #literal이 X타입이면
                        literal = literal.replace("X", "")
                        '''literal의 각 문자를 objectCode에 그대로 저장'''
                        for k in range(len(literal)):
                            token.object_code += str(literal[k]).upper()
                    self.code_list.append(token.object_code)
                else: #그 외 operator
                    token.object_code += token_table.make_object_code(j) #TokenTable에 정의된 메소드로 objectCode를 작성
                    self.code_list.append(token.object_code)
        '''for i, value in enumerate(self.code_list):
            print(value)'''
        i = 0
        while i <= self.section:
            for index, value in enumerate(self.Token_list[i].token_list):
                print(value.label + "\t" + value.operator + "\t" + value.operand[0].rstrip("\n")
                      + "\t" + value.comment.rstrip("\n")
                      + "\t\t\t" +value.object_code)
            i += 1

    '''작성된 codeList를 출력형태에 맞게 출력'''
    def print_object_code(self, file_name):
        f = open(file_name, 'w')
        buffer = "" #라인마다의 내용을 저장할 버퍼
        start_location = 0 #T라인이 시작할 때의 변수 주소를 저장
        ext_buffer_list = [] #ext변수를 저장할 공간
        ext_address_list = [] #ext변수의 주소를 저장
        word_buffer = "" #WORD 명령어에서 처리할 EQU 변수
        word_buffer_addr = 0 #EQU 변수의 주소를 저장

        '''각각의 프로그램을 의미하는 TokenList의 크기만큼 읽으며'''
        '''각각의 프로그램의 모든 object code를 읽어 버퍼에 누적하여 저장하면서 진행'''
        '''H,D,R,T,M라인의 형식에 맞는 문장을 만들기 위해 3개의 함수를 별도로 TokenTalbe 클래스에 정의'''
        '''버퍼에 내용을 저장하다 상황에 따라 버퍼를 매개변수로 알맞은 함수를 호출'''
        '''버퍼의 내용을 가공하여 H,D,R 또는 T 또는 M 라인의 형식에 맞는 형태로 바꾼 뒤 리턴'''
        '''리턴받은 문자열을 파일 입출력을 통해 저장한다'''
        for i, token_table in enumerate(self.Token_list):
            '''H, D, R라인 작성 '''
            f.write(token_table.make_HDR_line()) #새로운 TokenList을 가져오는 것은 새로운 프로그램을 가져오는 것을 의미
            '''T라인 작성'''
            for j, token in enumerate(token_table.token_list):
                if token.operator == "LTORG": #operator가 프로그램 중간에 나온 LTORG면 저장했던 내용을 T라인에 적음
                    if token_table.program_length > token.locctr + len(token.object_code):
                        buffer = token_table.make_T_line(buffer, start_location)
                        f.write(buffer)
                        buffer = ""
                elif token.operator == "WORD": #operator가 WORD면 word의 operand와 현재 주소를 저장
                    word_buffer += token.operand[0]
                    word_buffer_addr = token.locctr
                elif token.operator.find("+") != -1: #operator가 4형식이면 ext 변수리스트에 저장
                    ext_buffer_list.append(token.operand[0])
                    ext_address_list.append(token.locctr + 1)

                '''버퍼에 아무것도 없다는 것은 프로그램 시작이거나 기존 버퍼를 T라인에 적은 것이므로'''
                '''새로운 T라인을 위해 현재 주소를 저장해 둠'''
                if buffer == "":
                    start_location = token.locctr

                if (len(buffer) + len(token.object_code)) / 2 > 0X1D:
                    buffer = token_table.make_T_line(buffer, start_location)
                    f.write(buffer)
                    buffer = ""
                    start_location = token.locctr
                buffer += token.object_code

            buffer = token_table.make_T_line(buffer, start_location)
            f.write(buffer)
            buffer = ""

            buffer = token_table.make_M_line(ext_buffer_list, ext_address_list, word_buffer, word_buffer_addr)
            f.write(buffer)
            buffer = ""

            buffer = "E"
            if i == 0:
                buffer += "000000"
            buffer += "\n\n"
            f.write(buffer)
            buffer = ""

            ext_buffer_list.clear()
            ext_address_list.clear()
            word_buffer = ""
            word_buffer_addr = 0
        f.close()





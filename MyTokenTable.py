class TokenTable:
    '''bit 조작의 가독성을 위한 선언'''
    MAX_OPERAND = 3
    nFlag = 32
    iFlag = 16
    xFlag = 8
    bFlag = 4
    pFlag = 2
    eFlag = 1

    def __init__(self, symTab, instTab, literalTab):
        '''Token을 다룰 때 필요한 테이블들을 링크시킨다'''
        self.symTab = symTab
        self.instTab = instTab
        self.literalTab = literalTab
        self.token_list = [] #각 line을 의미별로 분할하고 분석하는 공간
        self.program_length = 0 #각 program의 길이를 저장하는 변수

    '''일반 문자열을 받아서 Token단위로 분리시켜 tokenList에 추가한다'''
    def put_token(self, line):
        token = Token(line)
        self.token_list.append(token)

    '''tokenList에서 index에 해당하는 Token을 리턴'''
    def get_token(self, token_index):
        return self.token_list[token_index]

    '''instruction table, symbol table literal table 등을 참조하여 objectcode를 생성하고, 이를 저장'''
    def make_object_code(self, token_index):
        object_code = "" #리턴할 완선된 object code
        token = self.get_token(token_index) #tokenList에서 토큰을 가져옴

        if token.operator.find("+") != -1: #operator가 4형식이면
            '''operator를 통해 instruction table에서 opcode를 가져옴'''
            '''opcode의 첫번째 바이트를 objectCode 첫번째 부분에 그대로 저장'''
            operator = token.operator.replace("+", "")
            opcode = self.instTab.get_opcode(operator)
            object_code += opcode[0]
            if token.operand[0].find(",") != -1: #operand에 loop가 있다면 nixbpe에 111001 저장
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 1)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 1)
            else: #operand에 loop가 없다면 nixbpe에 110001 저장
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 1)
            object_code += self.make_object_code_second_and_third(token_index, opcode) #objectCode의 2,3번째 부분을 저장
            object_code += "00000" #4형식은 operand의 주소를 모르기 때문에 나머지 부분은 0으로 저장
        elif self.instTab.get_format(token.operator) == "3/4": #operator가 3형식이면
            '''operator를 통해 instruction table에서 opcode를 가져옴'''
            '''opcode의 첫번째 바이트를 objectCode 첫번째 부분에 그대로 저장'''
            opcode = self.instTab.get_opcode(token.operator)
            object_code += opcode[0]
            if token.operand[0] == "": #RSUB과 같이 operand가 없다면 nixbpe에 110010 저장
                token.set_flag(TokenTable.nFlag, 1)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 1)
                token.set_flag(TokenTable.eFlag, 0)
                object_code += self.make_object_code_second_and_third(token_index, opcode)
            elif token.operand[0].find("#") != -1: #Immediate addressing이면 nixbpe에 110010 저장
                token.set_flag(TokenTable.nFlag, 0)
                token.set_flag(TokenTable.iFlag, 1)
                token.set_flag(TokenTable.xFlag, 0)
                token.set_flag(TokenTable.bFlag, 0)
                token.set_flag(TokenTable.pFlag, 0)
                token.set_flag(TokenTable.eFlag, 0)
                object_code += self.make_object_code_second_and_third(token_index, opcode) #objectCode의 2,3번째 부분을 저장

                operand = token.operand[0].replace("#", "") #operand를 16진수로 바꾸고 objectCode 나머지 부분에 그대로 저장
                disp = str(hex(int(operand)).upper().replace("0X", ""))
                '''6자리를 맞추기 위한 작업'''
                if len(disp) == 2:
                    object_code += "0"
                elif len(disp) == 1:
                    object_code += "00"
                object_code += disp
            else:
                if token.operand[0].find("@") != -1: #Indirect addressing이면 nixbpe에 100010 저장
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 0)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.symTab.search(token.operand[0]) #symbol table에서  operand의 주소를 가져옴
                elif token.operand[0].find("=") != -1: #operand가 literal이면 nixbpe에 110010 저장
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 1)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.literalTab.search(token.operand[0]) #literal table에서  operand의 주소를 가져옴
                else: #그 외 형식은 nixbpe에 110010 저장
                    token.set_flag(TokenTable.nFlag, 1)
                    token.set_flag(TokenTable.iFlag, 1)
                    token.set_flag(TokenTable.xFlag, 0)
                    token.set_flag(TokenTable.bFlag, 0)
                    token.set_flag(TokenTable.pFlag, 1)
                    token.set_flag(TokenTable.eFlag, 0)
                    pc = self.symTab.search(token.operand[0]) #symbol table에서  operand의 주소를 가져옴

                object_code += self.make_object_code_second_and_third(token_index, opcode) #objectCode의 2,3번째 부분을 저장
                '''가져온 operand의 주소와 현재 명령어 다음 locctr을 빼서 relative address를 구함'''
                '''16진수로 변환 후 objectCode에 저장'''
                target_address = pc - (token.locctr + 3)
                disp = target_address & 0xFFF #하위 3비트만 뽑아서 disp에 저장
                rest = str(hex(disp)).upper().replace("0X", "")
                '''6자리를 맞추기 위한 작업'''
                if len(rest) == 2:
                    object_code += "0"
                elif len(rest) == 1:
                    object_code += "00"
                object_code += rest
        else: #operator가 2형식이면
            '''operator를 통해 instruction table에서 opcode를 가져옴'''
            '''2형식이므로 opcode를 objectCode 1,2번째 부분에 그대로 저장'''
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

            '''operand의 개수에 따라 다르게 처리'''
            '''operand가 2개이면 각각을 확인하여 code값으로 변환 후 저장'''
            '''operand가 1개면 나머지 자리는 0으로 채움'''
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

    '''6자리 objectCode에서 2,3번째 값을 저장하는 함수'''
    '''tokenList에서 현재 토큰의 index와  opcode값을 매개변수로 받음'''
    def make_object_code_second_and_third(self, index, opcode):
        object_code_second_and_third = "" #리턴할 object code의 2, 3번째 문자열
        '''object code의 2번째 바이트 값을 구함'''
        ni = 0 #ni 비트를 구함
        if self.get_token(index).get_flag(TokenTable.nFlag) != 0:
            ni += 2
        if self.get_token(index).get_flag(TokenTable.iFlag) != 0:
            ni += 1

        '''opcode의 값과 ni 비트 값을 더하여 16진수 변환 후 object code의 2번째 바이트에 넣음'''
        if opcode[1] >= '0' and opcode[1] <= '9':
            ni += int(opcode[1])
            object_code_second_and_third += str(hex(ni)).upper().replace("0X","")
        else:
            ni += int(opcode[1], 16)
            object_code_second_and_third += str(hex(ni)).upper().replace("0X","")

        '''operand가 없다면 주소를 모르기 때문에 나머지자리에 0 저장 후 리턴'''
        if self.get_token(index).operand[0] == "":
            object_code_second_and_third += "0000"
            return object_code_second_and_third

        '''object code의 3번째 바이트 값을 구함'''
        xbpe = 0 #xbpe 비트를 구함
        if self.get_token(index).get_flag(TokenTable.xFlag) != 0:
            xbpe += TokenTable.xFlag
        if self.get_token(index).get_flag(TokenTable.bFlag) != 0:
            xbpe += TokenTable.bFlag
        if self.get_token(index).get_flag(TokenTable.pFlag) != 0:
            xbpe += TokenTable.pFlag
        if self.get_token(index).get_flag(TokenTable.eFlag) != 0:
            xbpe += TokenTable.eFlag
        #xbpe 비트 값을 16진수 변환 후 object code의 3번째 바이트에 넣음
        object_code_second_and_third += str(hex(xbpe)).upper().replace("0X", "")

        return object_code_second_and_third #완성된 문자열을 리턴

    '''print_object_code 메소드에서 호출하는 메소드'''
    '''object program에서 H,D,R라인에 들어갈 문자열을 만들고 리턴하는 메소드'''
    '''반복적 작업을 줄이기 위하여 모듈화'''
    def make_HDR_line(self):
        '''H라인 작성'''
        '''첫 시작으로 'H'문자와 프로그램 이름, 시작 주소, 프로그램의 길이를 문자열의 형태로 저장'''
        H_line = "H"+self.get_token(0).label+"\t000000" # H라인에 작성될 문자열
        program_length_to_str = str(hex(int(self.program_length))).upper().replace("0X", "") #각각의 프로그램의 길이를 문자열 형태로 바꿔 저장할 공간
        for i in range(6 - len(program_length_to_str)):
            H_line += "0"
        H_line += (program_length_to_str + "\n")

        '''D라인 작성'''
        '''extdef list에서 변수 이름과 주소를 가져옴'''
        '''주소를 16진수로 변환 후 6자리를 맞추고 이름과 함께 문자열 형태로 저장'''
        D_line = ""
        if len(self.symTab.extdef_list) != 0:
            D_line += "D" #첫 시작으로 'D'문자를 저장
            for i, ext_value in enumerate(self.symTab.extdef_list):
                extdef = ext_value.split(",")
                for j in range(len(extdef)):
                    location = str(hex(self.symTab.search(extdef[j]))).upper().replace("0X", "")
                    D_line += extdef[j].rstrip("\n")
                    for k in range(6 - len(location)):
                        D_line += "0"
                    D_line += location
            D_line += "\n"

        '''D라인 작성'''
        '''extdef list에서 변수 이름과 주소를 가져옴'''
        '''주소를 16진수로 변환 후 6자리를 맞추고 이름과 함께 문자열 형태로 저장'''
        R_line = "R" #첫 시작으로 'R'문자를 저장
        for i, ext_value in enumerate(self.symTab.extref_list):
            extref = ext_value.split(",")
            for j in range(len(extref)):
                R_line += extref[j]

        '''최종적으로 각각의 라인에 들어갈 문자열들을 합쳐서 하나의 문자열로 리턴'''
        '''호출한 print_object_code에서 리턴받은 문자열을 파일에 출력'''
        return H_line + D_line + R_line

    '''print_object_code 메소드에서 호출하는 메소드'''
    '''object program에서 T라인에 들어갈 문자열을 만들고 리턴하는 메소드'''
    '''매개변수로 각 T라인에 저장된 object code들이 저장된 버퍼와 시작 주소를 받음'''
    '''반복적 작업을 줄이기 위하여 모듈화'''
    def make_T_line(self, buffer, location):
        T_line = "T" # T라인에 작성될 문자열
        address = str(hex(location)).upper().replace("0X", "") # T라인 첫 명령어의 주소를 16진수 변환 후 문자열 형태로 저장
        cnt_of_char = str(hex(int(len(buffer)/2))).upper().replace("0X", "") # T라인의 문자의 개수를 16진수 변환 후 문자열 형태로 저장

        '''6자리를 맞추기 위한 작업'''
        for i in range(6 - len(address)):
            T_line += "0"
        T_line += address

        '''자릿수를 맞추기 위한 작업'''
        for i in range(2 - len(cnt_of_char)):
            T_line += "0"
        T_line += cnt_of_char

        '''T라인의 형식에 맞춰 문자'T',시작 주소, 문자의 개수가 저장된 문자열과'''
        '''object code들이 저장된 버퍼를 합쳐서 리턴'''
        '''호출한 print_object_code에서 리턴받은 문자열을 파일에 출력'''
        return T_line + buffer +"\n"

    '''print_object_code 메소드에서 호출하는 메소드'''
    '''object program에서 T라인에 들어갈 문자열을 만들고 리턴하는 메소드'''
    '''매개변수로 ext와 word 변수리스트와 각 변수들의 주소를 받음'''
    '''반복적 작업을 줄이기 위하여 모듈화'''
    def make_M_line(self, ext_buffer_list, ext_address_list, word_buffer, word_address):
        M_line = "" # M라인에 작성될 문자열
        '''ext 변수 개수만큼 진행'''
        for i , value in enumerate(ext_buffer_list):
            value = value.rstrip("\n")
            M_line += "M" #첫 시작으로 'M'문자를 저장
            '''ext 변수의 주소를 16진수 변환 후 저장한 뒤 문자열에 이어붙임'''
            ext_address = str(hex(ext_address_list[i])).upper().replace("0X", "")
            '''6자리를 맞추기 위한 작업'''
            for j in range(6 - len(ext_address)):
                M_line += "0"
            M_line += ext_address + "05+"
            '''ext 변수를 문자열에 이어붙임'''
            ''',X와 같은 loop가 있다면 해당 부분은 무시'''
            if value.find(",") != -1:
                only_buffer = value.split(",")
                M_line += only_buffer[0] + "\n"
            else:
                M_line += value + "\n"

        '''word 변수가 있다면 word 변수 개수만큼 진행'''
        if len(word_buffer) != 0:
            word_buffers = word_buffer.split("-")
            word_address_to_str = str(hex(word_address)).upper().replace("0X", "")
            for i in range(len(word_buffers)):
                M_line += "M"
                '''word 변수의 주소를 16진수 변환 후 저장한 뒤 문자열에 이어붙임'''
                '''6자리를 맞추기 위한 작업'''
                for j in range(6 - len(word_address_to_str)):
                    M_line += "0"
                M_line += word_address_to_str
                if i == 0:
                    M_line += "06+" + word_buffers[i] + "\n"
                else:
                    M_line += "06-" + word_buffers[i]

        '''M라인의 형식에 맞춰 문자'M',변수 주소,고쳐야 할 문자의 개수, 변수 이름이 저장된 문자열을 리턴'''
        '''호출한 print_object_code에서 리턴받은 문자열을 파일에 출력'''
        return M_line

'''각 라인별로 저장된 코드를 단어 단위로 분할한 후  의미를 해석하는 데에 사용되는 변수와 연산을 정의'''
'''의미 해석이 끝나면 pass2에서 object code로 변형되었을 때의 바이트 코드 역시 저장한다'''
class Token:
    def __init__(self, line):
        '''의미 분석 단계에서 사용되는 변수들'''
        '''클래스를 초기화 하면서 바로 line의 의미 분석을 수행한다'''
        self.nixbpe = 0X00 # 000000으로 초기화
        self.object_code = ""
        self.operand = []
        self.label = ""
        self.operator = ""
        self.operand.append("")
        self.comment = ""
        self.parsing(line)

    '''line의 실질적인 분석을 수행하는 함수. Token의 각 변수에 분석한 결과를 저장한다'''
    def parsing(self, line):
        parsed_line = line.split("\t") # tab문자를 기준으로 문자열을 나눔

        if parsed_line[0] == '.': #주석이면 넘어감
            return

        '''tab문자로 나눠진 문자열 각각의 순서에 맞게 파싱하여 저장'''
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

    '''n,i,x,b,p,e flag를 설정한다'''
    def set_flag(self, flag, value):
        if value == 1: # 집어넣고자 하는 값이 1일때만 진행
            self.nixbpe = self.nixbpe | flag # 바꾸고자 하는 위치의 비트와 논리합을 통해 비트를 집어넣음

    '''원하는 flag들의 값을 얻어온다'''
    '''비트위치에 들어가 있는 값. 플래그별로 각각 32, 16, 8, 4, 2, 1의 값을 리턴'''
    def get_flag(self, flags):
        return self.nixbpe & flags

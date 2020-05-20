class InstTable: #모든 instruction의 정보를 관리하는 클래스. instruction data들을 저장하는 클래스

    '''inst.data 파일을 불러와 저장'''
    def __init__(self, filename):
        self.file_name = filename
        self.inst_map = {} #inst.data 파일을 불러와 저장하는 공간하며 명령어의 이름을 집어넣으면 해당하는 Instruction의 정보들을 리턴
        self.open_file()

    '''파싱을 동시에 처리'''
    '''입력받은 이름의 파일을 열고 해당 내용을 파싱하여 inst_map에 저장'''
    def open_file(self):
        f = open(self.file_name, 'r')
        lines = f.readlines()
        for line in lines:
            instruction = Instruction()
            instruction.parsing(line)
            self.inst_map[instruction.name] = instruction
        f.close()

    '''추가한 메소드'''
    '''해당하는 instruction의 형식을 리턴'''
    def get_format(self, instruction_name):
        return self.inst_map[instruction_name].format

    '''추가한 메소드'''
    '''해당하는 instruction의 opcode를 리턴'''
    def get_opcode(self, instruction_name):
        return self.inst_map[instruction_name].opcode

class Instruction: #명령어 하나하나의 구체적인 정보를 저장하는 클래스
    def __init__(self):
        self.name = "" # instruction의 이름
        self.format = "" # instruction이 몇 바이트 명령어인지 저장
        self.opcode = "" # instruction의 opcode

    '''일반 문자열을 파싱하여 instruction 정보를 파악하고 저장'''
    def parsing(self, line):
        parsed_line = line.split("-") # inst.data의 항목을 '-'로 구분하였기 때문에 '-'문자를 기준으로 문자열을 나눔
        '''해당하는 항목의 정보를 저장'''
        self.name += parsed_line[0]
        self.format += parsed_line[1]
        self.opcode += parsed_line[2]


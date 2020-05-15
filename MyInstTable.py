class InstTable:
    def __init__(self, filename):
        self.file_name = filename
        self.inst_map = {}

    def open_file(self):
        f = open(self.file_name, 'r')
        lines = f.readlines()
        for line in lines:
            instruction = Instruction()
            instruction.parsing(line)
            self.inst_map[instruction.name] = instruction
        f.close()

    def save(self, index):
        # 추후 수정 필요
        self.name_list.append(self.instruction.name)
        self.format_list.append(self.instruction.format)
        self.opcode_list.append(self.instruction.opcode)
        self.name_map[self.instruction.name] = index
        index += 1
        # 추후 수정 필요

    def get_format(self, instruction_name):
        instruction = self.inst_map[instruction_name]
        return instruction.get_format()

    def get_opcode(self, instruction_name):
        instruction = self.inst_map[instruction_name]
        return instruction.get_opcode(self.inst_map[instruction_name])

class Instruction:
    def __init__(self):
        self.name = ""
        self.format = ""
        self.opcode = ""

    def parsing(self, line):
        parsedLine = line.split("-")
        self.name += parsedLine[0]
        self.format += parsedLine[1]
        self.opcode += parsedLine[2]
        #print(self.name +" "+self.format+" "+self.opcode+" ")

    def get_format(self):
        return self.format

    def get_opcode(self):
        return self.opcode


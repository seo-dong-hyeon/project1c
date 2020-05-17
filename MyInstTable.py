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

    def get_format(self, instruction_name):
        return self.inst_map[instruction_name].format

    def get_opcode(self, instruction_name):
        return self.inst_map[instruction_name].opcode

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


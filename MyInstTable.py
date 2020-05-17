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
        parsed_line = line.split("-")
        self.name += parsed_line[0]
        self.format += parsed_line[1]
        self.opcode += parsed_line[2]


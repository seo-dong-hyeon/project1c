class InstTable:
    def __init__(self, filename):
        self.inst_map = {}
        self.open_file(self, filename)

    def open_file(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        instruction = Instruction
        for line in lines:
            instruction.parsing(instruction, line)
            self.inst_map[instruction.name] = instruction
        f.close()

    def get_opcode(self, instruction_name):
        instruction = self.inst_map[instruction_name]
        return instruction.get_opcode(self.inst_map[instruction_name])

class Instruction:
    def parsing(self, line):
        parsedLine = line.split("-")
        self.name = parsedLine[0]
        self.format = parsedLine[1]
        self.opcode = parsedLine[2]
        #print(self.name +" "+self.format+" "+self.opcode+" ")

    def get_opcode(self):
        return self.opcode;

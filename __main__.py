from MyAssembler import Assembler

if __name__ == "__main__":
    assembler = Assembler
    assembler.__init__(assembler)
    assembler.load_input_file(assembler,'input.txt')
    assembler.pass1(assembler)

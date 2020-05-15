from MyAssembler import Assembler

if __name__ == "__main__":
    assembler = Assembler()
    assembler.load_input_file('input.txt')
    assembler.pass1()

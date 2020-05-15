from MyAssembler import Assembler

if __name__ == "__main__":
    assembler = Assembler()
    assembler.load_input_file('input.txt')
    assembler.pass1()
    assembler.print_symbol_table("symtab_20152382");
    assembler.print_literal_table("literaltab_20152382");

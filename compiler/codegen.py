#!/usr/bin/env python3

"""
	author: abhinavmufc, sidd607
	last modified: 25 October 2017
	revision: 0.1.5
"""

from semant import run_semant
from utils import print_ast
import ast

inbuilt_functions = {
    "in_int" :   "",
    "in_string" :   "",
    "out_int" :   "",
    "out_string" :   "",
    "abort" :   "",
    "copy" :   "",
    "type_name" :   ""
}

def io_out_string(arg):
    pass

class CodeGen:

    def __init__(self, sourcefile):
        self.ast = run_semant(sourcefile)
        print(self.ast)
        self.out_file = sourcefile + ".asm"

        

    def write(self, s, n=0):
        line = ""
        line += "\t"*n
        line += s 
        line += "\n"
        with open(self.out_file, "a") as f:
            f.write(line)
        
    
    def add_initial(self):
        """ Adding initial Global Data """
        
        self.write(".data", 0)
        main_class = ()
        for cl in self.ast:
            if cl.name == "Main":
                main_class = cl
                break
        if cl == ():
            raise Exception("No Main Class !!")
        self.main_class = cl
        print("----------------")
        print(self.main_class)
        print("----------------")

        for feature in main_class.features:
            if isinstance(feature, ast.Attribute):
                data_type = ""
                value = ""
                flag = False
                if feature.type == "Int":
                    data_type = ".word"
                    value  = "0"
                    flag = True
                elif feature.type == "String":
                    data_type = ".asciiz"
                    value = ""
                    flag = True
                
                if flag:
                    s = "\tmain_" + feature.ident.name + ": " + data_type + " " + value
                    self.write(s, 1)
                    print(s)
                
    def push_reg(self, r):
        x = "\t\tsw " + r + " 0($sp) # push " + r + " (step 1) " + "\n\t\t" + "addiu $sp $sp -4 # push " + r + " (step 2) " + "\n"
        return x

    def pop_reg(self, r):
        x = "\t\tlw " + r + " 4($sp) # pop " + r + " (step 1) " + "\n\t\t" + "addiu $sp $sp 4 # pop " + r + " (step 2) " + "\n"
        return x

    def add_binary_operation(self,stmt):
        self.write("#starting binary operation")
        if stmt.operator == '+':
            self.add_statement(stmt.left)
            self.write(self.push_reg("$a0"),0)
            self.add_statement(stmt.right)
            self.write(self.pop_reg("$t1"),0)
            self.write("addu $a0 $a0 $t1",0)
    
    def add_left_value(self,stmt):
        pass

    def add_statement(self,stmt):
        if isinstance(stmt,ast.Assignment):
            self.add_statement(stmt.expr)
            self.add_left_value(stmt.ident)
        if isinstance(stmt,ast.BinaryOperation):
            self.add_binary_operation(stmt)
        if isinstance(stmt,ast.Ident):
            self.write("lw $a0 " + str(4 * 1) + "($fp)\n")
        if isinstance(stmt, ast.FunctionCall):
            tmp = ""
            tmp += "# Function call sequence begin\n"+self.push_reg("$fp")
            self.write(tmp)
            self.add_args(stmt.params) 
            tmp = "jal main_" + stmt.ident.name+"\n"
            tmp += "# Function call sequence ends"
            self.write(tmp)
        if isinstance(stmt, int):
            x = "li $a0 " + str(stmt)
            self.write(x)

    def add_args(self, params):
        for i in params:
            self.add_statement(i)
            self.write(self.push_reg("$a0"))
            

    def add_function(self, method,cl):
        """ Adding Funtion """
        line = cl + "_" + method.ident.name + ":"
        self.write(line, 1)
        common_fun_starter = "move $fp $sp \n" + self.push_reg("$ra")
        self.write(common_fun_starter,2)
        #How to add arguments. GOD KNOWS!
        # for i in range(2,)
        # add_statement()
        ele = method.expr.elements
        for i in ele:
            self.add_statement(i)
        common_fun_ender = self.pop_reg("$ra")+"move $sp $fp # restore stack pointer to the beginning of the current stack frame\n lw $fp 0($sp) # restore frame pointer to its previous value\n jr $ra # jump back to the caller\n" 
        self.write(common_fun_ender)




    def traverse_function(self):
        """ Adding all functions other than Main """
        
        for i in self.main_class.features:
            if isinstance(i, ast.Method):
                if i.ident.name not in inbuilt_functions and i.ident.name != "main":
                    self.add_function(i, "main")
                    print("\n\n")
                    print(i)


    def add_main_elements(self):
        self.write(".text", 0)
        self.write("main: ", 1)
        self.write("move $fp, $sp", 2)
        main_block = ()
        for feature in self.main_class.features:
            if isinstance(feature, ast.Method) and feature.ident.name == 'main':
                print (feature)
                main_block = feature
                break

        if main_block ==():
            raise Exception("No Main function definied")


        for element in main_block.expr.elements:
            if isinstance(element, ast.FunctionCall):
                self.add_statement(element)
        self.add_final()



    def add_final(self):
        tmp = "li $v0, 10"
        self.write(tmp, 2)
        tmp = "syscall"
        self.write(tmp, 2)

    


def codegen(sourcefile):
    codeGen = CodeGen(sourcefile)
    codeGen.add_initial()    
    codeGen.add_main_elements()
    codeGen.traverse_function()
    

if __name__ == "__main__":
    import sys
    sourcefile = sys.argv[1]
    codegen(sourcefile)
import parser
import ast

class Semant:
        def __init__(self, sourcefile):

            self.classes_map = {}
            self.ast = parser.get_ast(sourcefile)
            self.inheritence_map = {}

        def populate_classes_map(self):

            for i in self.ast:
                self.classes_map[i.name] = i
            objc = ast.Type(name="Object", inherits="None",features=())
            ioc
            intc
            stringc
            boolc
            print(objc.name)

if __name__ == '__main__':

    import sys
    sourcefile = sys.argv[1]
    sem = Semant(sourcefile)
    sem.populate_classes_map()

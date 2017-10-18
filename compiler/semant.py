import parser
import ast
from collections import defaultdict

class Semant:
        def __init__(self, sourcefile):

            self.classes_map = {}
            self.ast = parser.get_ast(sourcefile)
            self.inheritance_graph = defaultdict(set)

        def populate_classes_map_and_inheritance_map(self):


            objc = ast.Type(name="Object", inherits="None",features=())
            ioc = ast.Type(name="IO", inherits="Object",features=())
            intc = ast.Type(name="Int", inherits="Object",features=())
            boolc = ast.Type(name="Bool", inherits="Object",features=())
            stringc = ast.Type(name="String", inherits="Object",features=())
            self.classes_map[objc.name] = objc
            self.classes_map[ioc.name] = ioc
            self.classes_map[intc.name] = intc
            self.classes_map[boolc.name] = boolc
            self.classes_map[stringc.name] = stringc
            for cl in self.ast:
                if cl.name in self.classes_map:
                    raise SemantError("class %s already defined" % cl.name)
                self.classes_map[cl.name] = cl
                if cl.name == "Object":
                    continue  # Object has no parent
                if cl.inherits:
                    self.inheritance_graph[cl.inherits].add(cl.name)
                else:
                    self.inheritance_graph["Object"].add(cl.name)
            # print (self.inheritance_graph)


if __name__ == '__main__':

    import sys
    sourcefile = sys.argv[1]
    sem = Semant(sourcefile)
    sem.populate_classes_map_and_inheritance_map()

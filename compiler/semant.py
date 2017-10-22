import parser
import ast
from collections import defaultdict
import warnings

class SemantError(Exception):
    pass


class SemantWarning(Warning):
    pass


class Semant:
        def __init__(self, sourcefile):

            self.classes_map = {}
            self.ast = parser.get_ast(sourcefile)
            self.inheritance_graph = defaultdict(set)

        def populate_classes_map_and_inheritance_map(self):

            print (self.ast)
            objc = ast.Type(name="Object", inherits="None",features=())
            ioc = ast.Type(name="IO", inherits="Object",features=())
            intc = ast.Type(name="Int", inherits="Object",features=())
            boolc = ast.Type(name="Bool", inherits="Object",features=())
            stringc = ast.Type(name="String", inherits="Object",features=())
            self.classes_map[objc.name] = objc
            self.classes_map[ioc.name] = ioc
            self.inheritance_graph["Object"].add(ioc.name)
            self.classes_map[intc.name] = intc
            self.inheritance_graph["Object"].add(intc.name)
            self.classes_map[boolc.name] = boolc
            self.inheritance_graph["Object"].add(boolc.name)
            self.classes_map[stringc.name] = stringc
            self.inheritance_graph["Object"].add(stringc.name)
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
        def check_for_undefined_classes(self):
            initial_parents = list(self.inheritance_graph.keys())
            for parentc in initial_parents:
                if parentc not in self.classes_map and parentc != "Object":
                    warnings.warn("classes %s inherit from an undefined parent %s" % (self.inheritance_graph[parentc], parentc), SemantWarning)
                    self.inheritance_graph['Object'] |= self.inheritance_graph[parentc]  # intermediate class does not exist so make these classes inherit from Object
                    del self.inheritance_graph[parentc]

        def impede_inheritance_from_base_classes(self):
            for parent in ['String', 'Int', 'Bool']:
                for cl_name in self.inheritance_graph[parent]:
                    raise SemantError("Class %s cannot inherit from base class %s" % (cl_name, parent))

        def visit_inheritance_tree(self,start_class,visited):
            visited[start_class] = True
            print(visited)
            if start_class not in self.inheritance_graph.keys():
                return True

            for childc in self.inheritance_graph[start_class]:
                #print("%s to %s" % (start_class, childc))
                self.visit_inheritance_tree(childc, visited)

            return True

        def check_for_inheritance_cycles(self):
            visited = {}
            for parent_name in self.inheritance_graph.keys():
                visited[parent_name] = False
                for cl_name in self.inheritance_graph[parent_name]:
                    visited[cl_name] = False
            self.visit_inheritance_tree("Object", visited)

            for k,v in visited.items():
                if not v:
                    raise SemantError("%s involved in an inheritance cycle." % k)


if __name__ == '__main__':

    import sys
    sourcefile = sys.argv[1]
    sem = Semant(sourcefile)
    sem.populate_classes_map_and_inheritance_map()
    sem.check_for_undefined_classes()
    sem.impede_inheritance_from_base_classes()
    sem.check_for_inheritance_cycles()

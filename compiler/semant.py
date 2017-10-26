"""  FUCKE UOUI """
import parser
import ast
from collections import defaultdict
import warnings
from collections import MutableMapping, Set
from ast import Attribute, Method
from copy import deepcopy
from utils import print_ast

class SemantError(Exception):
    pass


class SemantWarning(Warning):
    pass


class Semant:
        def __init__(self, sourcefile):

            self.classes_map = {}

            self.ast = parser.get_ast(sourcefile)
            #print(self.ast)

            self.inheritance_graph = defaultdict(set)

        def populate_classes_map_and_inheritance_map(self):

            #print (self.ast)
            objc = ast.Type(name="Object", inherits=None,features=())
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

        def check_scopes_and_infer_return_types(self,cl):
            variable_scopes  = [dict()]
            seen_attribute = set()
            seen_method = set()
            #Checking scopes
            for feature in cl.features:
                #print(feature)
                if isinstance(feature, ast.Attribute):
                    if feature.ident.name in seen_attribute:
                        raise SemantError("attribute %s is already defined" %feature.ident.name)
                    seen_attribute.add(feature.ident.name)
                    if feature.type == "SELF_TYPE":
                        variable_scopes[-1][feature.ident.name] = cl.type
                    else:
                        variable_scopes[-1][feature.ident.name] = feature.type #[-1] is for latest scope
            for feature in cl.features:
                if isinstance(feature,ast.Method):
                    if feature.ident.name in seen_method:
                        raise SemantError("method %s is already defined" % feature.name)
                    seen_method.add(feature.ident.name)
                    variable_scopes.append(dict()) #adding new scope

                    seen_formals = set()
                    for form in feature.formals:
                        if form.ident.name in seen_formals:
                            raise SemantError(("formal %s in method %s is already defined" % (formal[0], feature.name)));
                        seen_formals.add(form)
                        variable_scopes[-1][form.ident.name] = form.type
                    # traverse_expression(feature.body, variable_scopes, cl)
                    del variable_scopes[-1]
                # elif isinstance(feature, Attr):
                #     traverse_expression(feature.body, variable_scopes, cl)

            print (variable_scopes)
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')




        def expand_inherited_classes(self, start_class="Object"):
            """Apply inheritance rules through the class graph"""

            cl = self.classes_map[start_class]

            if cl.inherits:
                parent_cl = self.classes_map[cl.inherits]
                attr_set_child = [i for i in cl.features if isinstance(i, Attribute)]
                attr_set_parent = [i for i in parent_cl.features if isinstance(i, Attribute)]
                for attr in attr_set_child:
                    for pattr in attr_set_parent:
                        if attr.name == pattr.name:
                            raise SemantError("Attribute cannot be redefined in child class: " + cl.name + ", Attribute: " + attr.name)
                method_set_child = [i for i in cl.features if isinstance(i, Method)]
                method_set_parent = [i for i in parent_cl.features if isinstance(i, Method)]

                def extract_signatures(method_set):
                    method_signatures = {}
                    for method in method_set:
                        method_signatures[method.ident.name] = {}
                        for formal in method.formals:
                            method_signatures[method.ident.name][formal.ident.name] = formal.type
                        method_signatures[method.ident.name]['return'] = method.type
                    return method_signatures

                method_signatures_child = extract_signatures(method_set_child)
                method_signatures_parent = extract_signatures(method_set_parent)

                methods_in_child = set()

                for method in method_set_child:
                    methods_in_child.add(method.ident.name)
                    if method.ident.name in method_signatures_parent:
                        parent_signature = method_signatures_parent[method.ident.name]
                        child_signature = method_signatures_child[method.ident.name]
                        if parent_signature != child_signature:
                            raise SemantError("Redefined method %s cannot change arguments or return type of the parent method" % method.ident.name)

                for method in method_set_parent:
                    if method.ident.name not in methods_in_child:
                        new_method = deepcopy(method)

                        # TODO new_method.inherited_from = cl.parent  # used in codegen, to reuse function bodies
                        cl.features.append(new_method)
                for attr in attr_set_parent:
                    cl.features.append(deepcopy(attr))

            all_children = self.inheritance_graph[start_class]
            for child in all_children:
                self.expand_inherited_classes(child)

        def is_child(self,child_class, parent_class):
        """check whether childcl is a descendent of parentcl"""
            if child_class == parent_class:
                return True
            for cl in self.inheritance_graph[parent_class]:
                if is_child(child_class, cl):
                    return True
            return False
        def type_check(cl):
            '''Make sure the inferred types match the declared types'''
            for feature in cl.features:
                if isinstance(feature, Attribute):
                    if feature.type == "SELF_TYPE":
                        realtype = cl.name
                    else:
                        realtype = feature.type
                    if feature.expr:
                        type_check_expression(feature.body,cl)
                        child_type = feature.bpdy.return_type
                        pare_type = realtype
                    if not is_child(child_type,parent_type):
                        raise SemantError("Inferred type %s for attribute %s does not conform to declared type %s" % (child_type, feature.name, parent_type))


if __name__ == '__main__':

    import sys
    sourcefile = sys.argv[1]
    sem = Semant(sourcefile)
    sem.populate_classes_map_and_inheritance_map()
    sem.check_for_undefined_classes()
    sem.impede_inheritance_from_base_classes()
    sem.check_for_inheritance_cycles()
    print_ast(sem.ast)
    #print(sem.classes_map)
    for cl in sem.classes_map.values():
        sem.check_scopes_and_infer_return_types(cl)
    sem.expand_inherited_classes()
    #print("------------------------------------------------------")
    #print()
    #print_ast(sem.ast)

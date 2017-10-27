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
            self.method_map = {}

            self.ast = parser.get_ast(sourcefile)
            #print(self.ast)

            self.inheritance_graph = defaultdict(set)

        def populate_classes_map_and_inheritance_map(self):

            #print (self.ast)
            objc = ast.Type(name="Object", inherits=None,features=[
                ast.Method(ident = ast.Ident(name = 'abort'), type = 'Object', formals = (), expr = None),
                ast.Method(ident = ast.Ident(name = 'copy'), type = 'SELF_TYPE', formals = (), expr = None),
                ast.Method(ident = ast.Ident(name = 'type_name'), type = 'SELF_TYPE', formals = (), expr = None)
            ])
            ioc = ast.Type(name="IO", inherits="Object",features=[
                ast.Method(ident = ast.Ident(name = 'in_int'), type = 'SELF_TYPE', formals = (), expr = None),
                ast.Method(ident = ast.Ident(name = 'in_string'), type = 'SELF_TYPE', formals = (), expr = None),
                ast.Method(
                    ident = ast.Ident(name = 'out_int'),
                    type = 'SELF_TYPE',
                    formals = (
                        ast.Formal(ident = ast.Ident(name = 'arg'), type = 'Int'),
                    ),
                    expr = None
                ),
                ast.Method(
                    ident = ast.Ident(name = 'out_string'),
                    type = 'SELF_TYPE',
                    formals = (
                        ast.Formal(ast.Ident(name = 'arg'), type = 'String'),
                    ),
                    expr = None
                    )
            ])
            intc = ast.Type(name="Int", inherits="Object",features=[
                ast.Attribute(ident = ast.Ident(name = '_val'), type = 'Int', expr = None)
            ])
            boolc = ast.Type(name="Bool", inherits="Object",features=[
                ast.Attribute(ident = ast.Ident(name = '_val'), type = 'Bool', expr = None)
            ])
            stringc = ast.Type(name="String", inherits="Object",features=[
                ast.Attribute(ident = ast.Ident(name = '_val'), type = 'Int', expr = None),
                ast.Attribute(ident = ast.Ident(name = '_str_field'), type = 'SELF_TYPE', expr = None),
                ast.Method(ident = ast.Ident(name = 'length'), type = 'Int', formals = (), expr = None),
                ast.Method(
                    ident = ast.Ident(name = 'concat'), type = 'String',
                    formals = (
                        ast.Formal(ast.Ident(name = 'arg'), type = 'Int'),
                    ),
                    expr = None
                ),
                ast.Method(
                    ident = ast.Ident(name = 'substr'),
                    type = 'String',
                    formals = (
                        ast.Formal(ident = ast.Ident(name = 'arg1'), type = 'Int'),
                        ast.Formal(ident = ast.Ident(name = 'arg2'), type = 'Int')
                    ),
                    expr = None

                )
            ])
            self.ast = (objc,ioc, stringc, intc, boolc,) + self.ast
            # self.classes_map[objc.name] = objc
            # self.classes_map[ioc.name] = ioc
            # self.inheritance_graph["Object"].add(ioc.name)
            # self.classes_map[intc.name] = intc
            # self.inheritance_graph["Object"].add(intc.name)
            # self.classes_map[boolc.name] = boolc
            # self.inheritance_graph["Object"].add(boolc.name)
            # self.classes_map[stringc.name] = stringc
            # self.inheritance_graph["Object"].add(stringc.name)
            for cl in self.ast:
                print(cl)
                print("\n")
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


        def create_method_map(self):
            seen_method = dict()
            for cl in self.ast:
                for feature in cl.features:
                    if isinstance(feature, ast.Method):
                        tmp = (feature.ident.name, cl.name)
                        if tmp in seen_method:
                            raise SemantError("Method already defined: " + feature.ident.name)
                            return
                        seen_method[tmp] = feature.type
            for key in seen_method:
                print (key, seen_method[key])

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

                        variable_scopes[-1][feature.ident.name] = cl.name
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
                    self.traverse_expression(feature.expr, variable_scopes, cl)
                    del variable_scopes[-1]
                elif isinstance(feature, ast.Attribute):
                    self.traverse_expression(feature.expr, variable_scopes, cl)

            print (variable_scopes)



        def traverse_expression(self, expression, variable_scopes, cl):

            if isinstance(expression, ast.BinaryOperation):
                self.traverse_expression(expression.left, variable_scopes, cl)
                self.traverse_expression(expression.right, variable_scopes, cl)
                if expression.operator in ['<', '>', '==']:
                    expression.return_type = 'Bool'
                else:
                    expression.return_type = 'Int'
                print("***: ", expression.return_type, expression)


            elif isinstance(expression, ast.While):
                self.traverse_expression(expression.condition, variable_scopes, cl)
                self.traverse_expression(expression.action, variable_scopes, cl)
                print(expression.return_type, expression)
                print("***: ", expression.return_type, expression)

            elif isinstance(expression, ast.Block):
                last_type = None
                for expr in expression.elements:
                    self.traverse_expression(expr, variable_scopes, cl)
                    last_type = getattr(expr, 'return_type', None)
                expression.return_type = last_type
                print("***: ", expression.return_type, expression)

            elif isinstance(expression, ast.Assignment):
                self.traverse_expression(expression.expr, variable_scopes, cl)
                self.traverse_expression(expression.ident, variable_scopes, cl)
                expression.return_type = expression.ident.return_type
                print("***: ", expression.return_type, expression)

            elif isinstance(expression, ast.If):
                self.traverse_expression(expression.condition, variable_scopes, cl)
                self.traverse_expression(expression.true, variable_scopes, cl)
                self.traverse_expression(expression.false, variable_scopes, cl)
                print("\n\n\n",self.classes_map)
                print(expression.true)
                true_type = self.classes_map[expression.true.return_type]
                false_tyep = self.classes_map[expression.false.return_type]
                #ret_type = self.lowest_common_ancestor(true_type, false_tyep)
                #expression.return_type = ret_type
                print("***: ", expression.return_type, expression)

            elif isinstance(expression, ast.Case):
                pass

            elif isinstance(expression, ast.New):
                if expression.type == 'SELF_TYPE':
                    expression.return_type = cl.name
                    return
                expression.return_type = expression.type
                print("***: ", expression.return_type, expression)
            elif isinstance(expression, ast.Ident):
                for scope in variable_scopes[::-1]:
                    if expression.name in scope:
                        expression.return_type = scope[expression.name]
                        print("***: ", expression.return_type, expression)
                        return
                raise SemantError("Variable not declared in scope: " + expression.name + " in class: "+ cl.name)


            else:
                print("-----------------", expression)

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

        def type_check(self,cl):
            '''Make sure the inferred types match the declared types'''
            for feature in cl.features:
                if isinstance(feature, ast.Attribute):
                    print(feature)
                    if feature.type == "SELF_TYPE":
                        realtype = cl.name
                    else:
                        realtype = feature.type
                    if feature.expr:
                        self.type_check_expression(feature.expr,cl)
                        child_type = feature.expr.return_type
                        parent_type = realtype
                        if not self.is_child(child_type,parent_type):
                            raise SemantError("Inferred type %s for attribute %s does not conform to declared type %s" % (child_type, feature.ident.name, parent_type))
                elif isinstance(feature, Method):
                    for formal in feature.formals:
                        if formal.type == "SELF_TYPE":
                            raise SemantError("formal %s cannot have type SELF_TYPE" % formal[0])
                        elif formal.type not in self.classes_map:
                            raise SemantError("formal %s has a undefined type" % formal.ident.name)

                        if feature.type == "SELF_TYPE":
                            real_return_type = cl.name
                        else:
                            real_return_type = feature.type

                        if feature.expr is None:
                            if feature.type == "SELF_TYPE":
                                returned_type = cl.name
                            else:
                                returned_type = feature.type

                        else:
                            self.type_check_expression(feature.expr,cl)
                            returned_type = feature.type
                        if not self.is_child(returned_type,real_return_type):
                            raise SemantError("Inferred type %s for method %s does not conform to declared type %s") %(returned_type,feature.ident.name,real_return_type)

        def type_check_expression(self,expression,cl):
            '''make sure types validate at any point in the ast'''
            print(expression)
            if isinstance(expression,ast.Assignment):
                self.type_check_expression(expression.expr, cl)
                if not is_child(expression.expr.return_type, expression.ident.name.return_type):
                    raise SemantError("The inferred type %s for %s is not conformant to declared type %s" % (expression.expr.return_type, expression.ident.name, expression.name.return_type))
            elif isinstance(expression,ast.BinaryOperation):
                self.type_check_expression(expression.left,cl)
                self.type_check_expression(expression.right,cl)
                if not (self.is_child(expression.left.return_type, expression.right.return_type) or self.is_child(expression.right.return_type, expression.left.return_type)):
                    raise SemantError("The inferred type %s for %s is not conformant to declared type %s" % (expression.left.return_type, expression.ident.name, expression.right.return_type))

            elif isinstance(expression, ast.If):
                self.type_check_expression(expression.condition, cl)
                self.type_check_expression(expression.true, cl)
                self.type_check_expression(expression.false, cl)
                if expression.condition.return_type != "Bool":
                    raise SemantError("If statements must have boolean conditions")

            elif isinstance(expression, ast.Let):
                for line in expression.elements:
                    self.type_check_expression(line,cl)

            elif isinstance(expression, ast.While):
                self.type_check_expression(expression.condition,cl)
                self.type_check_expression(expression.body, cl)
                if expression.condition.return_type != "Bool":
                        raise SemantError("While statement must have boolean conditions")

            # elif isinstance(expression, MethodCall):
            #     self.type_check_expression(expression.expr, cl)
            #     # dispatch to current instance (self)
            #     if expression.expr == "self":
            #         bodycln = cl.name
            #     else:
            #         bodycln = expression.body.return_type
            #     # if isinstance(expression, StaticDispatch):
            #     #     # additional check on static dispatch
            #     #     if not is_conformant(bodycln, expression.type):
            #     #         raise SemantError("Static dispatch expression (before @Type) does not conform to declared type {}".format(expression.type))
            #
            #     called_method = None
            #     if bodycln in self.classes_map:
            #         bodycl = self.classes_map[bodycln]
            #         for feature in bodycl:
            #             if isinstance(feature, Method) and feature.ident.name == expression.method.ident.name:
            #                 called_method = feature
            #     if not called_method:
            #         raise SemantError("Tried to call the undefined method %s in class %s" % (expression.method.ident.name, bodycl.name))
            #     if len(expression.expr_list) != len(called_method.formal_list):
            #         raise SemantError("Tried to call method {} in class {} with wrong number of arguments".format(called_method.name, bodycl.name))
            #     else:
            #         # check conformance of arguments
            #         for expr, formal in zip(expression.expr_list, called_method.formal_list):
            #             if not is_conformant(expr.return_type, formal[1]):
            #                 raise SemantError("Argument {} passed to method {} in class {} is not conformant to its {} declaration".format(expr.return_type, called_method.ident.name, bodycl.name, formal[1]))


if __name__ == '__main__':

    import sys
    sourcefile = sys.argv[1]
    sem = Semant(sourcefile)
    sem.populate_classes_map_and_inheritance_map()
    sem.check_for_undefined_classes()
    sem.impede_inheritance_from_base_classes()
    sem.check_for_inheritance_cycles()
    print(sem.ast)
    print("---------------------")
    sem.create_method_map()
    print("---------------------")
    #print(sem.classes_map)
    for cl in sem.classes_map.values():
        sem.check_scopes_and_infer_return_types(cl)
    for cl in sem.classes_map.values():
        sem.type_check(cl)
    sem.expand_inherited_classes()
    print("------------------------------------------------------")
    #print(sem.ast)
    #print_ast(sem.ast)

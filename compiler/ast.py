from collections import namedtuple
from types import new_class

class Returnable:
    return_type = None

def returnable_namedtuple(type_name, fields):
    return new_class(type_name, (Returnable, namedtuple(type_name, fields)))

Assignment = returnable_namedtuple('Assignment', 'ident expr')
Attribute = returnable_namedtuple('Attribute', 'ident type expr')
BinaryOperation = returnable_namedtuple('BinaryOperation', 'operator left right')
Block = returnable_namedtuple('Block', 'elements')
Case = returnable_namedtuple('Case', 'expr typeactions')
Formal = returnable_namedtuple('Formal', 'ident type')
FunctionCall = returnable_namedtuple('FunctionCall', 'ident params')
Ident = returnable_namedtuple('Ident', 'name')
If = returnable_namedtuple('If', 'condition true false')
Let = returnable_namedtuple('Let', 'assignments expr')
MethodCall = returnable_namedtuple('MethodCall', 'object targettype method')
Method = returnable_namedtuple('Method', 'ident type formals expr')
New = returnable_namedtuple('New', 'type')
Type = returnable_namedtuple('Type', 'name inherits features')
TypeAction = returnable_namedtuple('TypeAction', 'ident type expr')
UnaryOperation = returnable_namedtuple('UnaryOperation', 'operator right')
While = returnable_namedtuple('While', 'condition action')
Self = returnable_namedtuple('Self','ident')

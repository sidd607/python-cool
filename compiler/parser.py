#!/usr/bin/env python3


"""
	author: abhinavmufc, sidd607
	last modified: 15 Sept 2017
	revision: 0.1.3
"""


import ply.yacc as yacc
import lexer
import ast
from utils import print_ast

tokens = lexer.tokens

# Grammar definitions in BNF form

precedence = (
    ('right', 'ASSIGN'),
    ('right', 'NOT'),
    ('nonassoc', 'LTEQ', 'LT', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'ISVOID'),
    ('right', 'INT_COMP'),
    ('left', 'AT'),
    ('left', 'DOT'),
)

def p_program(p):
    """program : classes"""
    #print("0000000000000000000000000")
    p[0] = p[1]

def p_classes(p):
    """classes : class
               | class classes"""
    #print("--------------------------------",p[0])
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_class(p):
    """class : CLASS TYPE inheritance LBRACE features_opt RBRACE SEMICOLON"""
    p[0] = ast.Type(name=p[2], inherits=p[3], features=p[5])


def p_inheritance(p):
    """inheritance : INHERITS TYPE
                   | empty"""

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_features_opt(p):
    """features_opt : features
                    | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_features(p):
    """features : feature
                | feature features"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_feature(p):
    """feature : ID LPAREN formals_opt RPAREN COLON TYPE LBRACE expr RBRACE SEMICOLON
               | attr_def SEMICOLON"""
    if len(p) == 11:
        p[0] = ast.Method(ident=ast.Ident(p[1]), type=p[6], formals=p[3], expr=p[8])
    elif len(p) == 3:
        p[0] = p[1]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_attr_defs(p):
    """attr_defs : attr_def
                 | attr_def COMMA attr_defs"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_attr_def(p):
    """attr_def : ID COLON TYPE assign_opt"""
    p[0] = ast.Attribute(ident=ast.Ident(p[1]), type=p[3], expr=p[4])

def p_assign_opt(p):
    """assign_opt : assign
                  | empty"""
    p[0] = p[1]

def p_assign(p):
    """assign : ASSIGN expr"""
    p[0] = p[2]

def p_formals_opt(p):
    """formals_opt : formals
                   | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_formals(p):
    """formals : formal
               | formal COMMA formals"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_formal(p):
    """formal : ID COLON TYPE"""
    p[0] = ast.Formal(ident=ast.Ident(p[1]), type=p[3])

def p_params_opt(p):
    """params_opt : params
                  | empty"""
    if p.slice[1].type == 'empty':
        p[0] = tuple()
    else:
        p[0] = p[1]

def p_params(p):
    """params : expr
              | expr COMMA params"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_block(p):
    """block : blockelements"""
    p[0] = ast.Block(p[1])

def p_blockelements(p):
    """blockelements : expr SEMICOLON
                     | expr SEMICOLON blockelements"""
    if len(p) == 3:
        p[0] = (p[1],)
    elif len(p) == 4:
        p[0] = (p[1],) + p[3]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_typeactions(p):
    """typeactions : typeaction
                   | typeaction typeactions"""
    if len(p) == 2:
        p[0] = (p[1],)
    elif len(p) == 3:
        p[0] = (p[1],) + p[2]
    else:
        raise SyntaxError('Invalid number of symbols')

def p_typeaction(p):
    """typeaction : ID COLON TYPE ACTION expr SEMICOLON"""
    p[0] = ast.TypeAction(ident=ast.Ident(p[1]), type=p[3], expr=p[5])

def p_function_call(p):
    """function_call : ID LPAREN params_opt RPAREN"""
    p[0] = ast.FunctionCall(ident=ast.Ident(p[1]), params=p[3])


def p_targettype_opt(p):
    """targettype_opt : targettype
                      | empty"""
    p[0] = p[1]

def p_targettype(p):
    """targettype : AT TYPE"""
    p[0] = p[2]

def p_expr_self(p):
    """expr  : SELF"""
    p[0] = ast.Self(ident=ast.Ident(p[1]))

def p_expr(p):
    """expr : ID assign
            | expr targettype_opt DOT function_call
            | function_call
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL
            | LET attr_defs IN expr
            | CASE expr OF typeactions ESAC
            | NEW TYPE
            | INT_COMP expr
            | NOT expr
            | ISVOID expr
            | expr PLUS expr
            | expr MINUS expr
            | expr MULTIPLY expr
            | expr DIVIDE expr
            | expr LT expr
            | expr LTEQ expr
            | expr EQ expr
            | LBRACE block RBRACE
            | LPAREN expr RPAREN
            | ID
            | INTEGER
            | STRING
            | BOOL
    """
    first_token = p.slice[1].type
    second_token = p.slice[2].type if len(p) > 2 else None
    third_token = p.slice[3].type if len(p) > 3 else None

    if first_token == 'ID':
        if second_token is None:
            p[0] = ast.Ident(p[1])
        elif second_token == 'assign':
            p[0] = ast.Assignment(ident=ast.Ident(p[1]), expr=p[2])
    elif first_token == 'expr':
        if len(p) == 4 and third_token == 'expr':
            p[0] = ast.BinaryOperation(operator=p[2], left=p[1], right=p[3])
        elif third_token == 'DOT':
            p[0] = ast.MethodCall(object=p[1], targettype=p[2], method=p[4])
    elif first_token == 'function_call':
        p[0] = p[1]
    elif first_token == 'IF':
        p[0] = ast.If(condition=p[2], true=p[4], false=p[6])
    elif first_token == 'WHILE':
        p[0] = ast.While(condition=p[2], action=p[4])
    elif first_token == 'LET':
        p[0] = ast.Let(assignments=p[2], expr=p[4])
    elif first_token == 'CASE':
        p[0] = ast.Case(expr=p[2], typeactions=p[4])
    elif first_token == 'NEW':
        p[0] = ast.New(p[2])
    elif first_token in ['ISVOID', 'INT_COMP', 'NOT']:
        p[0] = ast.UnaryOperation(operator=p[1], right=p[2])
    elif first_token in ['LBRACE', 'LPAREN']:
        p[0] = p[2]
    elif first_token in ['INTEGER', 'STRING', 'BOOL']:
        p[0] = p[1]

def p_empty(p):
    """empty :"""
    p[0] = None

def p_error(p):
    print('Syntax error in input at {!r}'.format(p))

# Create parser
yacc.yacc()

def get_ast(sourcefile):
	with open(sourcefile, 'r') as source:
		t = yacc.parse(source.read())
	return t

if __name__ == '__main__':

    import sys
    from pprint import pprint

    # Get file as argument

    if len(sys.argv) != 2:
        print('You need to specify a cool source file to read from.', file=sys.stderr)
        sys.exit(1)
    if not sys.argv[1].endswith('.cl'):
        print('Argument needs to be a cool source file ending on ".cl".', file=sys.stderr)
        sys.exit(1)

    sourcefile = sys.argv[1]

    # Read and parse source file

    with open(sourcefile, 'r') as source:
        t = yacc.parse(source.read())
    # Print AST
    print (t)
    print_ast(t)

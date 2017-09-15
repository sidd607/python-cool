#!/usr/bin/env python3


"""
	author: abhinavmufc, sidd607
	last modified: 1 Sept 2017
	revision: 0.1.3
"""

import ply.lex as lex


###### TOKEN LISTS ######

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',','=','<']

reserved = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'in': 'IN',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
	'self': 'SELF',
    'isvoid': 'ISVOID',
}

ignored = [' ', '\t']

tokens = [
    # Identifiers
    'TYPE', 'ID',
    # Primitive data types
    'INTEGER', 'STRING', 'BOOL',
    # Special keywords
    'ACTION',
    # Literals
     "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", "COMMA", "DOT", "SEMICOLON", "AT",
    # Operators
     "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", "INT_COMP", "NOT",
	# Comments
	"COMMENT",
] + list(reserved.values())


###### TOKEN RULES ######

# Primitive data types

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


def t_SINGLECOMMENT(t):
	r"\-\-[^\n]*"
	pass

## Lexer States

states = (("COMMENT", 'exclusive'),)


## Stateful comments (multiple lines)

def t_start_comment(t):
    r"\(\*"
    t.lexer.push_state("COMMENT")
    t.lexer.comment_count = 0

def t_COMMENT_startanother(t):
    r"\(\*"
    t.lexer.comment_count += 1

def t_COMMENT_newline(t):
	r'\n+'
	t.lexer.lineno +=len(t.value)

def t_COMMENT_end(t):
    r"\*\)"
    if t.lexer.comment_count == 0:
        t.lexer.pop_state()
    else:
        t.lexer.comment_count -= 1



def t_COMMENT_error(t):
    t.lexer.skip(1)

# Other tokens with precedence before TYPE and ID

def t_NOT(t):
    r'[nN][oO][tT]'
    return t

# Identifiers

def t_TYPE(t):
    r'[A-Z][A-Za-z0-9_]*'
    return t

def t_ID(t):
    r'[a-z][A-Za-z0-9_]*'
#   print(t.type)
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

#To increase the Line Count
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Operators

t_LPAREN = r'\('        # (
t_RPAREN = r'\)'        # )
t_LBRACE = r'\{'        # {
t_RBRACE = r'\}'        # }
t_COLON = r'\:'         # :
t_COMMA = r'\,'         # ,
t_DOT = r'\.'           # .
t_SEMICOLON = r'\;'     # ;
t_AT = r'\@'            # @
t_MULTIPLY = r'\*'      # *
t_DIVIDE = r'\/'        # /
t_PLUS = r'\+'          # +
t_MINUS = r'\-'         # -
t_INT_COMP = r'~'       # ~
t_LT = r'\<'            # <
t_EQ = r'\='            # =
t_LTEQ = r'\<\='        # <=
t_ASSIGN = r'\<\-'      # <-

t_ACTION = r'\=\>'       # =>

###### SPECIAL RULES ######

def t_error(t):
    print("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

t_ignore = ''.join(ignored)


###### CREATE LEXER ######

lex.lex()


###### PROCESS INPUT ######

if __name__ == '__main__':

    # Get file as argument

    import sys
    if len(sys.argv) != 2:
        print('You need to specify a cool source file to read from.', file=sys.stderr)
        sys.exit(1)
    if not sys.argv[1].endswith('.cl'):
        print('Argument needs to be a cool source file ending on ".cl".', file=sys.stderr)
        sys.exit(1)

    sourcefile = sys.argv[1]

    # Read source file

    with open(sourcefile, 'r') as source:
        lex.input(source.read())

    # Read tokens

    while True:
        token = lex.token()
        if token is None:
            break
        print(token)
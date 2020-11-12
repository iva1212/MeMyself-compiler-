reserved = {
   'int': 'NOM_INT',
   'float': 'NOM_FLOAT',
   'char': 'NOM_CHAR',
   'void':'VOID',
   'if' : 'IF',
   'then':'THEN',
   'else' : 'ELSE',
   'do':'DO',
   'to':'TO',
   'for':'FOR',
   'while':'WHILE',
   'program':'PROGRAM',
   'write':'WRITE',
   'read':'READ',
   'var':'VAR',
   'return':'RETURN',
   'main':'MAIN',
   'module':'MODULE',
   'func': 'FUNC',
   'Line':'LINE',
   'Point':'POINT',
   'Circle':'CIRCLE',
   'ArcUp':'ARCUP',
   'ArcDown':'ARCDOWN',
   'PenUp':'PENUP',
   'PenDown':'PENDOWN',
   'PenSize':'PENSIZE',
   'Color':'COLOR',
   'Clear':'CLEAR',
   'SetX': 'SETX',
   'SetY': 'SETY',
   'Right': 'RIGHT',
   'Left' : 'LEFT'
}
tokens = [
    'INT','FLOAT','CHAR','STRING','PLUS','MINUS','TIMES','DIVIDE','ID',
    'LSTHAN','MRTHAN','LSETHAN','MRETHAN','EQUALS','NOT_EQUALS','DOUBLE',
    'LPAREN','RPAREN','LBRACKET','RBRACKET','SEMICOLON','COMA','AND','OR'
 ] + list(reserved.values())

# Tokens
t_LSTHAN  = r'<'
t_MRTHAN  = r'>'
t_LSETHAN = r'<='
t_MRETHAN = r'>='
t_DOUBLE  = r'=='
t_EQUALS  = r'='
t_NOT_EQUALS = r'!='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET= r'\{'
t_RBRACKET= r'\}'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_SEMICOLON = r';'
t_COMA    =r'\,'
t_AND     =r'&'
t_OR      =r'\|'



def t_FLOAT(t):
    r'\-?\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t
def t_INT(t):
    r'\-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t
def t_CHAR(t):
  r'\'.\''
  t.value = t.value[1]
  return t
def t_STRING(t):
  r'\".*\"'
  return t
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t"
t_ignore_COMMENT = r'%%.*'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()


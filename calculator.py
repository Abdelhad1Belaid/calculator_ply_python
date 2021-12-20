import ply.lex as lex 
import ply.yacc as yacc 
import sys
 
 #This is not not fully functioning, but it's a calculator hehehe you can use variable assign like a = 3 ..
 
# Making the LEXER 

tokens = [
        'INT',
        'FLOAT',
        'IDENTIFIER',
        'PLUS',
        'MINUS',
        'DIVIDE',
        'MULTIPLY',
        'EQUALS'
        ]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_ignore = ' \t'


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFIER'
    return t


def t_error(t):
    print("Illegal char {} on line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


lexer = lex.lex()
'''
lexer.input("belaid = 1.4 + 3")
while True:
    tok = lexer.token()
    if not tok:
        break 
    print(tok)
'''

# Note : Tested and worked so perfect 


precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE')
        )


# Making the PARSER


def p_calc(p):
    '''
    calc : expression 
         | var_assign
         | empty 
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : IDENTIFIER EQUALS expression  
    '''
    p[0] = ('=', p[1], p[3])


def p_expression(p):
    '''
    expression : expression MULTIPLY expression 
               | expression DIVIDE expression 
               | expression PLUS expression 
               | expression MINUS expression 
    '''
    p[0] = (p[2], p[1], p[3])


def p_expression_int_float(p):
    '''
    expression : INT 
               | FLOAT 
    '''
    p[0] = p[1]


def p_expression_var(p):
    '''
    expression : IDENTIFIER
    '''
    p[0] = ('var', p[1])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("Syntax Error in Input !!", str(p))
    sys.exit(2)


yacc.yacc() 


env = {}


def run(p):
    global env 
    if type(p) == tuple:
        if p[0] == '+':
            return p[1] + run(p[2])
        elif p[0] == '-':
            return p[1] - run(p[2])
        elif p[0] == '*':
            return p[1] * run(p[2])
        elif p[0] == '/':
            return p[1] / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            return p[2]
        elif p[0] == 'var':
            if p[1] not in env:
                return "Undefined variable " + str(p[1]) 
            else:
                return env[p[1]]

    else:
        return p


print('''Hello User.
        This is a SIMPLE, DUMB calculator build by Abdelhadi Belaid \n
        during his solo learning journey about lexer & parser ...
        \n[Ctrl-D to exit ]''')


while True:
    try:
        expr = input(">>>")
    except EOFError:
        break 
    yacc.parse(expr)

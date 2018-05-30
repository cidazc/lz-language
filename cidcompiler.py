
#############################################################
###################  LEXICAL ANALYZER  ######################
#############################################################

import ply.lex as lex

#tokens part
tokens = [
   'NAME',

   'LESSEQ',
   'GREATEREQ',
   'GREATER',
   'LESS',
   'NOTEQ',
   'ASSIGN',
   'EQUALS',

   'PLUS',
   'MINUS',
   'TIMES',
   'FDIVIDE',
   'DIVIDE',
   'MODULO',
   'POWER',

   'LPAREN',
   'RPAREN',
   'LBRACKET',
   'RBRACKET',
   'COMMA',

   'STRING',
   'INT',
   'FLOAT',
   'COMMENT',

   'LZDIGIT',
   'LZWORD'
    ]

reserved = {
    'pr' : 'PRINT',
    'if' : 'IF',
    'el' : 'ELSE',
    'wh' : 'WHILE',

    'fi' : 'ENDIF',
    'le' : 'ENDELSE',
    'hw' : 'ENDWHILE',
    'rp' : 'ENDPRINT',
    'up' : 'ENDPUSH',

    'st' : 'STRINGDEC',
    'in' : 'INTDEC',
    'fl' : 'FLOATDEC',
    'ip' : 'INPUTDEC',

    'pu' : 'PUSH',
    'po' : 'POP',
    'to' : 'TOP',
    'pa' : 'PRINTARRAY',
    'em' : 'ISEMPTY',
    'ln' : 'ARRLEN',

    'an' : 'AND',
    'or' : 'OR',
    'no' : 'NOT',

    'nl' : 'NEWLINE'

}

lzdigit = {'wa':'0','oh':'1','to':'2','ti':'3','fo':'4','fi':'5','si':'6','se':'7','ei':'8','ni':'9','do':'.'}
lzword = {'0':'wa','1':'oh','2':'to','3':'ti','4':'fo','5':'fi','6':'si','7':'se','8':'ei','9':'ni','.':'do'}


tokens = tokens + reserved.values()


t_LESSEQ = r'\<\='
t_GREATEREQ = r'\>\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_NOTEQ = r'!\='
t_ASSIGN = r'='
t_EQUALS = r'\=\='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_FDIVIDE = r'//'
t_DIVIDE  = r'/'
t_MODULO  = r'%'
t_POWER  = r'\^'

# Delimiters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_COMMA            = r','

t_ignore = ' \t'

def t_COMMENT(t):
    r'\\.*'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_IF(t): r'if'; return t
def t_ELSE(t): r'el'; return t
def t_WHILE(t): r'wh'; return t

def t_ENDIF(t): r'fi'; return t
def t_ENDELSE(t): r'le'; return t
def t_ENDWHILE(t): r'hw'; return t
def t_ENDPRINT(t): r'rp'; return t
def t_ENDPUSH(t): r'up'; return t

def t_STRINGDEC(t): r'st'; return t
def t_INTDEC(t): r'in'; return t
def t_FLOATDEC(t): r'fl'; return t
def t_INPUTDEC(t): r'ip'; return t

def t_PUSH(t): r'pu'; return t
def t_POP(t): r'po'; return t
def t_TOP(t): r'to'; return t
def t_PRINTARRAY(t): r'pa'; return t
def t_ISEMPTY(t): r'em'; return t
def t_ARRLEN(t): r'ln'; return t


def t_AND(t): r'an'; return t
def t_OR(t): r'or'; return t
def t_NOT(t): r'no'; return t

def t_NEWLINE(t): r'nl'; return t

def t_LZDIGIT(t):
    r'`[0-9\.]+'
    t.value = str(t.value)
    t.value = t.value[1:]
    temp = ""
    while len(t.value) > 0:
        temp2 = t.value[:1]
        temp = temp + lzword[temp2]
        t.value = t.value[1:]
    t.value = temp
    temp2 = None
    temp = None
    return t

def t_LZWORD(t):
    r'`[a-z]*'
    t.value = t.value[1:]
    temp = ""
    dotExists = False
    while len(t.value) > 0:
        temp2 = t.value[:2]
        if temp2 == 'do':
            dotExists = True
        temp = temp + lzdigit[temp2]
        t.value = t.value[2:]
    if dotExists == True:
        t.value = float(temp)
    else:
        t.value = int(temp)
    return t

def t_STRING(t):
    r'\'[^\']*\''
    #if t.value.startswith('\'') and t.value.endswith('\''):
    t.value = (t.value)[1:-1]
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print 'Illegal character'
    t.lexer.skip(1)

lexer = lex.lex()


#############################################################
###################       PARSER       ######################
#############################################################


import ply.yacc as yacc
from sys import *



precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'FDIVIDE', 'MODULO','POWER'),
    ('if', 'IF'),
    ('left', 'ELSE'),
    ('right', 'UMINUS')
)

# dictionary of names (for storing variables)
names = {}
tempArr = []

################      STARTING GRAMMAR   #####################
def p_starting_code(p):
    ''' start : statements'''
    p[0] = p[1]
#FIRST RUN
    run(p[0])

#GRAMMAR FOR MULTIPLE LINES
def p_statements(p):
    ''' statements : statements statement
                    | statement'''
    if len(p) == 3:
        p[0] = ("statements",p[1],p[2])
    else:
        p[0] = p[1]

#GRAMMAR FOR STATEMENTS
def p_statement(p):
    ''' statement : var_dec
                    | if_statement
                    | ifel_statement
                    | wh_statement
                    | ip_statement
                    | pr_statement
                    | assign_expr
                    | arr_push
                    | arr_print
                    | new_line'''
    p[0] = p[1]
    pass

#GRAMMAR FOR ASSIGNING VALUES
def p_statement_assign(p):
    '''assign_expr : NAME ASSIGN expression'''
    p[0] = ("assign_expr", p[1],p[3],lexer.lineno)
    pass

#GRAMMAR FOR DECLARATIONS
def p_var_dec(p):
    ''' var_dec : var_dec_st
                | var_dec_in
                | var_dec_fl
                | arr_dec'''
    p[0] = p[1]
    pass

def p_var_dec_string(p):
    '''var_dec_st : NAME ASSIGN STRINGDEC STRING'''
    p[0] = ("dec_string", p[1], p[4],lexer.lineno)
    pass

def p_var_dec_int(p):
    '''var_dec_in : NAME ASSIGN INTDEC expression'''
    p[0] = ("dec_int", p[1], p[4],lexer.lineno)
    pass

def p_var_dec_float(p):
    '''var_dec_fl : NAME ASSIGN FLOATDEC expression'''
    p[0] = ("dec_float", p[1], p[4],lexer.lineno)
    pass


def p_arr_dec(p):
    '''arr_dec : NAME ASSIGN LBRACKET arr_param RBRACKET
                | NAME ASSIGN LBRACKET RBRACKET'''
    if len(p) == 6:
        p[0] = ("arr_dec", p[1], p[4])
    else:
        p[0] = ("arr_dec_empty", p[1])
    pass

def p_arr_parameters(p):
    '''arr_param : arr_param COMMA arr_thing
                    | arr_thing '''
    if len(p) == 4:
        p[0] = ("arr_param_multiple", p[1],p[3])
    else:
        p[0] = ("arr_param_single", p[1])
    pass

def p_arr_thing(p):
    '''arr_thing : STRING
                    | expression'''
    p[0] = p[1]
    pass


#GRAMMAR FOR INPUT AND OUTPUT
def p_statement_input(p):
    '''ip_statement : INPUTDEC NAME'''
    p[0] = ("input", p[2],lexer.lineno)
    pass

def p_statement_print(p):
    '''pr_statement : PRINT outputblock ENDPRINT'''
    p[0] = ("pr", p[2])
    pass

def p_statement_newline(p):
    '''new_line : NEWLINE'''
    p[0] = ("print_new_line", p[1])
    pass


def p_outputblock(p):
    '''outputblock : outputblock expression
                    | outputblock STRING
                    | outputblock comparison
                    | outputblock LZDIGIT
                    | expression
                    | STRING
                    | comparison
                    | LZDIGIT'''
    if len(p) == 3:
        p[0] = ("multiprint", p[1], p[2])
    else:
        p[0] = p[1]
    pass

#GRAMMAR FOR CONDITIONALS AND LOOPS
def p_statement_if(p):
    '''if_statement : IF LBRACKET comparison RBRACKET statements ENDIF'''
    p[0] = ("if",p[3],p[5])
    pass

def p_statement_ifel(p):
    '''ifel_statement : IF LBRACKET comparison RBRACKET statements ENDIF ELSE statements ENDELSE'''
    p[0] = ("ifel",p[3],p[5],p[8])
    pass

def p_statement_while(p):
    'wh_statement : WHILE LBRACKET comparison RBRACKET statements ENDWHILE'
    p[0] = ("wh", p[3],p[5])
    pass



#GRAMMAR FOR COMPARISONS
def p_comparison_empty(p):
    '''comparison : arr_empty'''
    p[0] = p[1]
    pass

def p_comparison_group(p):
    '''comparison : LBRACKET comparison RBRACKET'''
    p[0] = p[2]
    pass

def p_comparison_binop(p):
    '''comparison : expression EQUALS expression
                          | expression NOTEQ expression
                          | expression GREATER expression
                          | expression LESS expression
                          | expression GREATEREQ expression
                          | expression LESSEQ expression'''
    p[0] = ("binarycompare",p[1], p[2],p[3])
    pass

def p_comparison_and(p):
    '''comparison : comparison AND comparison'''
    p[0] = ("log_and",p[1], p[3])
    pass

def p_comparison_or(p):
    '''comparison : comparison OR comparison'''
    p[0] = ("log_or",p[1], p[3])
    pass

def p_comparison_not(p):
    '''comparison : NOT comparison'''
    p[0] = ("log_not",p[2])
    pass


#GRAMMAR FOR EXPRESSIONS AND ARITHMETIC WITH THEM
def p_expression_binaryoperators(p):
    '''expression : expression PLUS expression
                          | expression MINUS expression
                          | expression TIMES expression
                          | expression FDIVIDE expression
                          | expression DIVIDE expression
                          | expression MODULO expression
                          | expression POWER expression'''
    p[0] = ("binop", p[1], p[2], p[3])
    pass

def p_groupedexpression(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]
    pass

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]
    pass

def p_expression_number(p):
    '''expression : INT
                    | FLOAT
                    | LZWORD'''
    p[0] = p[1]
    pass

def p_expression_name(p):
    'expression : NAME'
    p[0] = ("names", p[1], lexer.lineno)
    pass

#GRAMMAR FOR ARRAY OPERATIONS
def p_arr_access(p):
    'expression : NAME LBRACKET expression RBRACKET'
    p[0] = ("arr_access", p[1],p[3],lexer.lineno)
    pass

def p_arr_push(p):
    'arr_push : PUSH NAME expression ENDPUSH'
    p[0] = ("arr_push", p[2],p[3],lexer.lineno)
    pass

def p_arr_print(p):
    'arr_print : PRINTARRAY NAME'
    p[0] = ("arr_print", p[2],lexer.lineno)
    pass

def p_arr_pop(p):
    'expression : POP NAME'
    p[0] = ("arr_pop", p[2], lexer.lineno)
    pass

def p_arr_top(p):
    'expression : TOP NAME'
    p[0] = ("arr_top", p[2], lexer.lineno)
    pass

def p_arr_empty(p):
    'arr_empty : ISEMPTY NAME'
    p[0] = ("arr_empty", p[2], lexer.lineno)
    pass

def p_arr_len(p):
    'expression : ARRLEN NAME'
    p[0] = ("arr_len", p[2], lexer.lineno)
    pass

def p_arr_update(p):
    'statement : NAME LBRACKET expression RBRACKET ASSIGN expression'
    p[0] = ("arr_update", p[1],p[3],p[6], lexer.lineno)
    pass


#############################################################
################      AST EVALUATION    #####################
#############################################################

def run(p):
    #print("pumasok sa run")
    global names
    global tempArr
    #print(p)
    #print(names)
    if type(p) == tuple:
#CONDITIONALS
        if p[0] == "if" or p[0] == "ifel":
            #print("nagrurun si if")
            if run(p[1]) == True:
                #print("true sa if")
                run(p[2])
            elif run(p[1]) == False and run(p[0]) == "ifel":
                #print("di siya true sa if")
                run(p[3])
#LOOPS
        elif p[0] == "wh":
            #print("while loop na siya")
            while run(p[1]) == True:
                #print("loop still true")
                run(p[2])
#BOOLEAN EXPRESSIONS
        elif p[0] == "binarycompare":
            #print("doing binary compare")
            if p[2] == '==':
                return run(p[1]) == run(p[3])
            elif p[2] == '!=':
                return run(p[1]) != run(p[3])
            elif p[2] == '>':
                return run(p[1]) > run(p[3])
            elif p[2] == '<':
                return run(p[1]) < run(p[3])
            elif p[2] == '>=':
                return run(p[1]) >= run(p[3])
            elif p[2] == '<=':
                return run(p[1]) <= run(p[3])
        elif p[0] == "log_and":
            return run(p[1]) and run(p[3])
        elif p[0] == "log_or":
            return run(p[1]) or run(p[3])
        elif p[0] == "log_not":
                return not(run(p[1]))
#OPERATIONS
        elif p[0] == "binop":
            if p[2] == '+':
                #print("nasa plus")
                return (run(p[1]) + run(p[3]))
            elif p[2] == '-':
                return (run(p[1]) - run(p[3]))
            elif p[2] == '*':
                return (run(p[1]) * run(p[3]))
            elif p[2] == '//':
                if run(p[3]) == 0:
                    print("Arithmetic Error, cannot divide by 0")
                    exit()
                else:
                    return int(run(p[1]) / run(p[3]))
            elif p[2] == '/':
                if p[3] == 0:
                    print("Arithmetic Error, cannot divide by 0")
                    exit()
                else:
                    return ((run(p[1])*1.0) / (run(p[3])*1.0))
            elif p[2] == '%':
                return run(p[1]) % run(p[3])
            elif p[2] == '^':
                return pow(run(p[1]),run(p[3]))
#PRINT
        elif p[0] == "pr":
            temp = run(p[1])
            if temp != None:
                print(temp)
        elif p[0] == "multiprint":
            tempOne = run(p[1])
            tempTwo = run(p[2])
            if tempOne is not None:
                print(tempOne),
            if tempTwo is not None:
                print(tempTwo),
            tempOne = None
            tempTwo = None
        elif p[0] == "print_new_line":
            print ("")
        #INPUT
        elif p[0] == "input":
                if p[1] not in names:
                    print "Variable name " + p[1] + " at line " + str(p[3]-1) + " does not exist, please use an existing name"
                    exit()
                else:
                    tempZing = input()
                    if type(names[p[1]]) == int:
                        names[p[1]] = int(tempZing)
                    elif type(names[p[1]]) == float:
                        names[p[1]] = float(tempZing)
                    else:
                        names[p[1]] = tempZing
#DECLARATIONS
        elif p[0] == "dec_string":
            if p[1] not in names:
                tempString = run(p[2])
                if type(tempString) == str:
                    names[run(p[1])] = run(p[2])
                else:
                    print "The input at line no " + str(p[3]-1) + " is not a string"
                    exit()
                tempString = None
            else:
                print "Variable name " + p[1] + " at line " + str(p[3]-1) + " already in use, please use another name"
                exit()
        elif p[0] == "dec_int":
            if p[1] not in names:
                tempInt = int(run(p[2]))
                tempFloat = float(run(p[2]))
                if tempFloat == tempInt:
                    names[run(p[1])] = tempInt
                else:
                    print "The input at line no " + str(p[3]-1) + " is not an int"
                    exit()
            else:
                print "Variable name " + p[1] + " at line " + str(p[3]-1) + " already in use, please use another name"
                exit()
        elif p[0] == "dec_float":
            if p[1] not in names:
                names[run(p[1])] = float(run(p[2]))
            else:
                print "Variable name " + p[1] + " at line " + str(p[3]-1) + " already in use, please use another name"
                exit()
#ARRAY RUN STUFF
        elif p[0] == "arr_dec":
            tempArr.append(run(p[2]))
            tempArr.pop()
            names[p[1]] = tempArr
            #print(names[p[1]])
            tempArr = []
        elif p[0] == "arr_dec_empty":
            tempArr = []
            names[p[1]] = tempArr
            #print(names[p[1]])
        elif p[0] == "arr_param_multiple":
            tempValOne = run(p[1])
            tempValTwo = run(p[2])
            if tempValOne != None:
                tempArr.append(tempValOne)
            if tempValTwo != None:
                tempArr.append(tempValTwo)
            tempValOne = None
            tempValTwo = None
        elif p[0] == "arr_param_single":
            tempValOne = run(p[1])
            if tempValOne is not None:
                tempArr.append(tempValOne)
            tempValOne = None
        elif p[0] == "arr_access":
            solveIndex = run(p[2])
            #print "p[1] is " + p[1]
            #print names
            if p[1] in names:
                if type(names[p[1]]) == list:
                    if type(solveIndex) == int:
                        #print("nasa loob", solveIndex, p[1])
                        if solveIndex < len (names[p[1]]):
                            return names[p[1]][solveIndex]
                        else:
                            print "Array index out of bounds exception at line " +str(p[3]-1)+" accessing value "+str(solveIndex)+" but array only until "+str(len(names[p[1]])-1)
                            exit()
                    else:
                        print "Wrong array index type at line" + str(p[3]-1)
                        exit()
                    solveIndex = None
                else:
                    print "Variable "+p[1]+" is not an array. Error at line "+str(p[3]-1)
                    exit()
            else:
                print "Variable "+p[1]+" does not exist. Error at line "+str(p[3]-1)
        elif p[0] == "arr_update":
            solveIndex = run(p[2])
            if p[1] in names:
                if type(names[p[1]]) == list:
                    if type(solveIndex) == int:
                        if solveIndex < len (names[p[1]]):
                            names[p[1]][solveIndex] = run(p[3])
                        else:
                            print "Array index out of bounds exception at line " +str(p[4]-1)+" accessing value "+str(solveIndex)+" but array only until "+str(len(names[p[4]])-1)
                            exit()
                    else:
                        print "Wrong array index type at line" + str(p[4]-1)
                        exit()
                    solveIndex = None
                else:
                    print "Variable "+p[1]+" is not an array. Error at line "+str(p[4]-1)
                    exit()
            else:
                print "Variable "+p[1]+" does not exist. Error at line "+str(p[3]-1)
        elif p[0] == "arr_push":
            if p[1] in names:
                if type(names[p[1]]) != list:
                    print "Variable "+p[1]+" is not an array. Error at line "+str(p[3]-1)
                    exit()
                else:
                    names[p[1]].append(run(p[2]))
                    #print(names[p[1]])
            else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()

        elif p[0] == "arr_pop":
                if p[1] in names:
                    if type(names[p[1]]) != list:
                        print "Variable "+p[1]+" is not an array. Error at line "+str(p[2]-1)
                        exit()
                    else:
                        if len(names[p[1]]) != 0:
                            tempVar = names[p[1]].pop()
                            #print("eyyy",tempVar)
                            return tempVar
                        else:
                            print "Array "+p[1]+" is empty. Error at line "+str(p[2]-1)
                            exit()
                else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()
        elif p[0] == "arr_top":
                if p[1] in names:
                    if type(names[p[1]]) != list:
                        print "Variable "+p[1]+" is not an array. Error at line "+str(p[2]-1)
                        exit()
                    else:
                        if len(names[p[1]]) != 0:
                            tempVar = names[p[1]][len(names[p[1]])-1]
                            return tempVar
                        else:
                            print "Array "+p[1]+" is empty. Error at line "+str(p[2]-1)
                            exit()
                else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()
        elif p[0] == "arr_empty":
                if p[1] in names:
                    if type(names[p[1]]) != list:
                        print "Variable "+p[1]+" is not an array. Error at line "+str(p[2]-1)
                        exit()
                    else:
                        tempVar = len(names[p[1]])
                        if tempVar == 0:
                            return True
                        else:
                            return False
                else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()
        elif p[0] == "arr_len":
                if p[1] in names:
                    if type(names[p[1]]) != list:
                        print "Variable "+p[1]+" is not an array. Error at line "+str(p[2]-1)
                        exit()
                    else:
                        tempVar = len(names[p[1]])
                        return tempVar
                else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()
        elif p[0] == "arr_print":
                if p[1] in names:
                    if type(names[p[1]]) != list:
                        print "Variable "+p[1]+" is not an array. Error at line "+str(p[2]-1)
                        exit()
                    else:
                        print(names[p[1]])
                else:
                    print "Variable "+p[1]+" not found . Error at line "+str(p[3]-1)
                    exit()
        elif p[0] == "assign_expr":
            if p[1] in names:
                names[p[1]] = run(p[2])
            else:
                print "Undeclared variable " + p[1] + " at line no ", str(p[3]-1)
                exit()
        elif p[0] == "names":
            if p[1] in names:
                return names[p[1]]
            else:
                print "Undeclared variable " + p[1] + " at line no ", str(p[2]-1)
                exit()
        elif p[0] == "statements":
            run(p[1])
            run(p[2])
    else:
            return p
    pass

#SYNTAX ERRORS
def p_error(p):
    print("Syntax error in input!")
    exit()
    pass

#BUILDING THE PARSER
parser = yacc.yacc()

#OPENING THE FILE
filename = open(argv[1],"r")

while True:
    try:
        s = filename.read()
        if s == "":
            break
    except EOFError:
        break
    parser.parse(s)

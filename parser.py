from lexer import tokens
import config
from collections import deque
from cuboSemantico import cuboSemantico
from tablaFunciones import tablaFunciones
from cuadruplos import Cuadruplos
# Parsing rules

tablaFunc = tablaFunciones()
cuads = Cuadruplos(tablaFunc)
listaVariables = []
tipoActual = ""
tipoRetorno = ""



precedence = (
    ('nonassoc', 'LSTHAN', 'MRTHAN','LSETHAN','MRETHAN'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )
# dictionary of names
names = { }
start = 'programa'

def p_programa(t):
    '''programa : PROGRAM  inicio_programa agregar_cuad_main SEMICOLON vars funs MAIN LPAREN RPAREN completar_cuad_main bloque
                | PROGRAM  inicio_programa agregar_cuad_main SEMICOLON vars MAIN LPAREN RPAREN completar_cuad_main bloque
    '''
    cuads.agregarFinPro()
    tablaFunc.printVariables()
    cuads.imprimirCuads()
    cuads.build()
def p_inicio_programa(t):
    '''inicio_programa : ID
    '''
    tablaFunc.agregarFuncion("main",'void')
    tablaFunc.setFuncActual("main")
    tablaFunc.setFuncGlobal()
def p_vars_start(t):
    '''vars : VAR vars2 
            | empty'''
    
def p_vars_cycle(t):
    '''vars2 : tipo id_var SEMICOLON agregar_variable vars2
             | tipo id_var SEMICOLON agregar_variable '''
             
def p_id_var(t):
    '''id_var : ID agregar_lstvar COMA id_var
              | ID agregar_lstvar'''
    
def p_tipo(t):
    '''tipo : NOM_INT
            | NOM_FLOAT
            | NOM_CHAR'''
    global tipoActual
    tipoActual = t[1]
def p_tipo_func(t):
    '''tipo_func : VOID
                 | NOM_INT
                 | NOM_FLOAT
                 | NOM_CHAR
    '''
    global tipoRetorno
    tipoRetorno = t[1]

def p_funs_start(t):
    '''funs : FUNC tipo_func funs2
    '''
def p_funs_end(t):
    '''funs2 : MODULE  ID agregar_funs LPAREN parametros RPAREN vars  bloque finalizar_funs
             | MODULE  ID agregar_funs LPAREN parametros RPAREN vars  bloque finalizar_funs funs
    '''
def p_parametros(t):
    '''parametros : tipo ID agregar_param COMA parametros
                  | tipo ID agregar_param
                  | empty
    '''

def p_bloque_start(t):
    '''bloque : LBRACKET bloque1 RBRACKET
              | LBRACKET RBRACKET '''
def p_bloque_end(t):
    '''bloque1 : estatuto bloque1
               | empty '''
def p_estatuto(t):
    '''estatuto : asignacion
                | modulo_v
                | return
                | lectura
                | escritura
                | desicion
                | repeticion
                | func_esp
                '''
def p_asignacion(t):
    '''asignacion : exp_var EQUALS agregar_exp_op expresion SEMICOLON agregar_cuad_asign
    '''
def p_modulo_v(t):
    ''' modulo_v : ID agregar_cuad_era LPAREN e RPAREN fin_func SEMICOLON
                 | ID agregar_cuad_era LPAREN RPAREN fin_func SEMICOLON
    ''' 
def p_return(t):
    ''' return : RETURN LPAREN exp RPAREN SEMICOLON 
    '''
    cuads.agregarReturn()
def p_lectura(t):
    ''' lectura : READ LPAREN exp_var agregar_cuad_read lectura2
    '''

def p_lectura_cyclo(t):
    ''' lectura2 : COMA exp_var agregar_cuad_read lectura2
                 | RPAREN SEMICOLON
    '''
def p_func_esp(t):
    ''' func_esp : func_esp_name_param   LPAREN exp RPAREN agregar_cuad_esp_param_func  SEMICOLON
                 | func_esp_name_no_param   LPAREN RPAREN agregar_cuad_esp_no_param_func SEMICOLON
                 | COLOR agregar_esp_func LPAREN exp COMA exp COMA exp RPAREN agregar_cuad_esp_param_func SEMICOLON
    '''
def p_e(t):
    ''' e : exp agregar_param_check  COMA e
          | exp agregar_param_check
    '''
def p_func_esp_name_param(t):
    '''func_esp_name_param : LINE agregar_esp_func
                     | POINT agregar_esp_func
                     | CIRCLE agregar_esp_func
                     | ARCUP agregar_esp_func
                     | ARCDOWN agregar_esp_func
                     | SETX agregar_esp_func
                     | SETY agregar_esp_func
                     | RIGHT agregar_esp_func
                     | LEFT agregar_esp_func
                     | PENSIZE agregar_esp_func
    '''
def p_func_esp_name_no_param(t):
    '''func_esp_name_no_param : PENUP agregar_esp_func
                           | PENDOWN agregar_esp_func
                           | CLEAR agregar_esp_func
    '''
def p_escritura_start(t):
    ''' escritura : WRITE LPAREN escritura2 RPAREN SEMICOLON
    '''
def p_escritura_cycle(t):
    '''escritura2 : expresion agregar_cuad_print_exp COMA escritura2
                  | STRING agregar_cuad_print_str COMA escritura2
                  | expresion agregar_cuad_print_exp
                  | STRING agregar_cuad_print_str
    '''
def p_decision(t):
    '''desicion : IF LPAREN expresion RPAREN agregar_cuad_if THEN bloque
                | IF LPAREN expresion RPAREN agregar_cuad_if THEN bloque else
    '''
    cuads.completarIf()
def p_desicion_else(t):
    '''else : ELSE agregar_cuad_else bloque
    '''
    pass
def p_var_cte(t):
    '''var_cte : INT
               | FLOAT
               | CHAR
    '''
    tipo = None
    if (type(t[1]) is int):
        tipo = 'int'
    elif (type(t[1]) is float):
        tipo = 'float'
    elif (type(t[1]) is str):
        tipo = 'char'
    cte = cuads.guardarCte(t[1], tipo)
    cuads.agregarCte(cte)
    
def p_repeticion(t):
    '''repeticion : condicional
                  | no_condicional 
    '''
def p_condicional(t):
    '''condicional : WHILE agregar_while LPAREN expresion RPAREN agregar_while_cond DO bloque
    '''
    cuads.terminarLoop()
def p_no_condicional(t):
    '''no_condicional : FOR ID agregar_for_var EQUALS exp igualar_for_var TO exp agregar_for_cond DO bloque
    '''
    cuads.agregarFor()
def p_expresion(t):
    '''expresion : exp_comp agregar_cuad_log exp_log '''
def p_exp_log(t):
    '''exp_log :   AND agregar_exp_op expresion
                 | OR agregar_exp_op expresion
                 | empty
    '''
def p_exp_comp(t):
    '''exp_comp   : exp  agregar_cuad_comp
                 | exp  agregar_cuad_comp MRTHAN agregar_exp_op exp_comp
                 | exp  agregar_cuad_comp LSTHAN agregar_exp_op exp_comp
                 | exp  agregar_cuad_comp LSETHAN agregar_exp_op exp_comp
                 | exp  agregar_cuad_comp MRETHAN agregar_exp_op exp_comp
                 | exp  agregar_cuad_comp DOUBLE agregar_exp_op exp_comp
                 | exp  agregar_cuad_comp NOT_EQUALS agregar_exp_op exp_comp
    '''
def p_exp(t):
    '''exp : termino agregar_cuad_arith
           | termino agregar_cuad_arith PLUS agregar_exp_op exp
           | termino agregar_cuad_arith MINUS agregar_exp_op exp'''
def p_termino(t):
    '''termino : factor agregar_cuad_factor
               | factor agregar_cuad_factor TIMES agregar_exp_op termino
               | factor agregar_cuad_factor DIVIDE agregar_exp_op termino '''
def p_factor(t):
    '''factor : factor_paren
              | PLUS var_cte 
              | MINUS var_cte
              | return_func
              | var_cte 
              | exp_var'''
def p_factor_paren(t):
    '''factor_paren : LPAREN agregar_exp_op expresion RPAREN '''
    cuads.popOperador()
def p_return_func(t):
    ''' return_func : ID agregar_cuad_era LPAREN e RPAREN fin_func
                    | ID agregar_cuad_era LPAREN  RPAREN fin_func '''
    cuads.agregarRetFunc()
def p_exp_var(t):
    ''' exp_var : ID '''
    var = tablaFunc.buscarVariable(t[1],tablaFunc.funcActual)
    cuads.agregarVar(var)

def p_empty(t):
    'empty :'
    pass

# Funciones para puntos neurologicos
#Se agrega la funcion a la tabla de funciones
def p_agregar_funs(t):
    '''agregar_funs : empty
    '''
    global tipoRetorno
    resFunc = tablaFunc.agregarFuncion(t[-1],tipoRetorno)
    if resFunc != "OK":
        raise Exception(f'Funcion {resFunc}() Ya existe!')
    tablaFunc.setFuncActual(t[-1])
    tablaFunc.setStartCuad(cuads.cuads_totales)
    tipoRetorno =""
def p_agregar_param(t):
    ''' agregar_param : empty '''
    param = t[-1]
    if not tablaFunc.existeVar(param,tablaFunc.funcActual):
        vDir = cuads.vDir.guardarEspacio(tablaFunc.funcActual,tipoActual)
        tablaFunc.agregarVariable(param,vDir,tipoActual)
        tablaFunc.agregarParam(vDir,tipoActual)
    else:
        s_error(f'Multiple declaration of "{param}"!')
#Se agrega operador a la pila de operadores
def p_agregar_exp_op(t):
    ''' agregar_exp_op : empty '''
    cuads.agregarOperador(t[-1])
#Se agrega variable a la lista de variables temporal.
def p_agregar_var(t):
    ''' agregar_lstvar : empty '''
    global listaVariables
    if(tablaFunc.funcActual == tablaFunc.funcGlobal):
        listaVariables.append((t[-1],cuads.vDir.guardarEspacio('global',tipoActual)))
    else:
        listaVariables.append((t[-1],cuads.vDir.guardarEspacio(tablaFunc.funcActual,tipoActual)))
#Se agrega variable a la tabla de variables de la funcion actual
def p_agregar_variable(t):
    '''agregar_variable : empty
    '''
    global listaVariables
    global tipoActual

    var = tablaFunc.agregarVariables(listaVariables,tipoActual)
    if var != 'OK':
        s_error(f'Variable "{var}" ya existe!"')
    listaVariables = []
def p_agregar_cuad_main(t):
    ''' agregar_cuad_main : empty'''
    cuads.agregarMain()
def p_completar_cuad_main(t):
    ''' completar_cuad_main : empty '''
    cuads.completarMain()
    tablaFunc.setFuncActual("main")
def p_agregar_cuad_log(t):
    ''' agregar_cuad_log : empty'''
    cuads.agregarExp(['&','|'])
def p_agregar_cuad_comp(t):
    ''' agregar_cuad_comp : empty '''
    cuads.agregarExp(['==', '!=', '<', '<=', '>', '>='])
def p_agregar_cuad_arith(t):
    '''  agregar_cuad_arith : empty '''
    cuads.agregarExp(['+', '-'])
def p_agregar_cuad_factor(t):
    ''' agregar_cuad_factor : empty  '''
    cuads.agregarExp(['*', '/'])
def p_agregar_cuad_asign(t):
    ''' agregar_cuad_asign : empty '''
    cuads.agregarAsignacion()
def p_agregar_cuad_read(t):
    ''' agregar_cuad_read : empty '''
    cuads.agregarRead()
def p_agregar_cuad_print_str(t):
    ''' agregar_cuad_print_str : empty'''
    cuads.agregarPrint(t[-1])
def p_agregar_cuad_print_exp(t):
    ''' agregar_cuad_print_exp : empty'''
    cuads.agregarPrint(False)
def p_agregar_cuad_if(t):
    ''' agregar_cuad_if : empty '''
    cuads.agregarIf()
def p_agregar_cuad_else(t):
    ''' agregar_cuad_else : empty '''
    cuads.agregarElse()
def p_agregar_for_var(t):
    ''' agregar_for_var : empty '''
    cuads.agregarForVar(t[-1])
def p_igualar_for_var(t):
    ''' igualar_for_var : empty '''
    cuads.igualarForVar()
def p_agregar_for_cond(t):
    ''' agregar_for_cond : empty'''
    cuads.agregarForCond()
def p_agregar_while(t):
    ''' agregar_while : empty '''
    cuads.agregarWhile()
def p_agregar_while_cond(t):
    ''' agregar_while_cond : empty '''
    cuads.agregarIf()
def p_finalizar_funs(t):
    ''' finalizar_funs : empty '''
    cuads.agregarFinFunc()
def p_agregar_cuad_Era(t):
    ''' agregar_cuad_era : empty '''
    func = t[-1]
    if tablaFunc.funcionExiste(func):
        cuads.agregarEra(func)
        cuads.agregarFunc(func)
        cuads.pOperadores.append('(')
    else:
        raise Exception(f'Funcion {func}() no existe!')
def p_agregar_param_check(t):
    ''' agregar_param_check : empty '''
    try:
        param = tablaFunc.getParam(cuads.getTopFunc())
    except :
        raise Exception(f'({cuads.getTopFunc()}) Parameters missmatch!')
    cuads.agregarParam(param,tablaFunc.count_param)
    tablaFunc.incrementarParam()
def p_fin_func(t):
    ''' fin_func : empty '''
    func = cuads.getTopFunc()
    if tablaFunc.verificarParams(func):
        tablaFunc.resetParamCount()
        cuads.agregarFuncSub(func,tablaFunc.getStartCuad(func))
        cuads.popOperador()
def p_agregar_esp_func(t):
    ''' agregar_esp_func : empty'''
    cuads.agregarFunc(t[-1])
def p_agregar_cuad_esp_func(t):
    ''' agregar_cuad_esp_param_func : empty '''
    cuads.agregarEspFunc()
def p_agregar_cuad_esp_no_param_func(t):
    ''' agregar_cuad_esp_no_param_func : empty '''
    cuads.agregarCuad((cuads.pFuncs.pop(),None,None,None))
def p_error(t):
  raise Exception(f'({t.lineno}) Syntax error at "{t.value}"')
def s_error(t):
    raise Exception(t)

import ply.yacc as yacc
parser = yacc.yacc()

f = open(config.nombre_archivo+'.txt','r')
data = f.read()
f.close()

parser.parse(data)


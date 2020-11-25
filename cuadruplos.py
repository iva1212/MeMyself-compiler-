from manejadorDirecciones import manejadorDirecciones
from cuboSemantico import cuboSemantico
from collections import deque
import config
class Cuad_Var:
  def __init__(self, var_id, var_dir, tipo):
    self.id = var_id
    self.dir = var_dir
    self.tipo = tipo

class Cuadruplos:
    def __init__(self, dir_func):
        self.dir_func = dir_func
        self.cuboSem = cuboSemantico()
        self.vDir = manejadorDirecciones()
        self.cuads = deque()
        self.pVars = deque()
        self.pOperadores = deque()
        self.pSaltos = deque()
        self.pFuncs = deque()
        self.cuads_totales = 0
        self.cont_temporales = 0
        self.cont_return = 0
    
    def guardarVar(self,valor,tipo):
        if  self.dir_func.buscarVariable(valor,self.dir_func.funcActual):
            vDir = self.vDir.guardarEspacio(self.dir_func.funcActual, tipo)
            self.dir_func.agregarVariable(valor, tipo, vDir)
        return self.dir_func.buscarVariable(valor,self.dir_func.funcActual )
    def agregarVar(self, var):
        cvar = Cuad_Var(var["id_var"], var["vDir"], var["tipo"])
        self.pVars.append(cvar)
    def agregarTemporal(self,tipo,var_dir):
        cvar = Cuad_Var(f't{self.cont_temporales}', var_dir, tipo)
        self.pVars.append(cvar)

    def agregarOperador(self, op):
        self.pOperadores.append(op)
    def agregarCte(self,cte):
        cVar = Cuad_Var(cte.valor, cte.vDir, cte.tipo)
        self.pVars.append(cVar)
    def popOperador(self):
        self.pOperadores.pop()
    def popFuncion(self):
        self.pFuncs.pop()
    def guardarCte(self,valor,tipo):
        if not self.dir_func.existeCte(valor, tipo):
            vDir = self.vDir.guardarEspacio('cte', tipo)
            self.dir_func.agregarCte(valor, tipo, vDir)
        return self.dir_func.getCte(valor, tipo)
    
        # Append dual-operand operation quad
    def agregarCuad(self,cuad):
        self.cuads.append(cuad)
        self.cuads_totales += 1
    def completarCuad(self,num,salto):
        cuadLlenar = list(self.cuads[num])
        cuadLlenar[3] = salto
        self.cuads[num] = tuple(cuadLlenar)
    def agregarExp(self, ops):
        if not self.pOperadores or self.pOperadores[-1] not in ops: # si el stack esta vacio, no seguir o si no esta en las operadores
            return

        der = self.pVars.pop()
        izq = self.pVars.pop()
        op = self.pOperadores.pop()

        tipo_temp = self.cuboSem.obtenerSem(izq.tipo, der.tipo, op)
        if tipo_temp == 'error':
            raise Exception(f'Type mismatch! {izq.tipo} {op} {der.tipo}')


        res = self.vDir.guardarEspacio('temp', tipo_temp)
        self.agregarCuad((op, izq.dir, der.dir, res))
        self.agregarTemporal(tipo_temp,res)

        self.cont_temporales += 1
    def agregarAsignacion(self):
        der = self.pVars.pop()
        izq = self.pVars.pop()
        op = self.pOperadores.pop()

        tipo_temp = self.cuboSem.obtenerSem(izq.tipo, der.tipo, op)
        if tipo_temp == 'error':
            raise Exception(f'Type mismatch! {izq.tipo} {op} {der.tipo}')

        self.agregarCuad((op, der.dir, None, izq.dir))
    def agregarRead(self):
        var = self.pVars.pop()
        self.agregarCuad(('READ', var.id, None, var.dir))
    def agregarPrint(self, string):
        # Strings simply use this case and stop here
        if string:
            self.agregarCuad(('WRITE', None, None, string))
            return

        var = self.pVars.pop()
        self.agregarCuad(('WRITE', None, None, var.dir))
    def agregarIf(self):
        res = self.pVars.pop()
        if res.tipo == 'bool':
            self.agregarCuad(('GoToF', res.dir, None, None))
            self.pSaltos.append(self.cuads_totales - 1)
        else:
            raise Exception(f'Type mismatch! {res.tipo}')
    def agregarElse(self):
        self.agregarCuad(('GoTo', None, None, None))
        salto = self.pSaltos.pop()
        self.pSaltos.append(self.cuads_totales - 1)
        self.completarCuad(salto, self.cuads_totales)
    def completarIf(self):
        res = self.pSaltos.pop()
        self.completarCuad(res,self.cuads_totales)
    def agregarForVar(self,var):
        self.dir_func.agregarVariable(var,self.vDir.guardarEspacio('temp', 'int'),'int')
        for_var= self.guardarVar(var,'int')
        self.agregarVar(for_var)
        self.agregarVar(for_var)
        self.agregarVar(for_var)
    def igualarForVar(self):
        self.agregarOperador('=')
        self.agregarAsignacion()
        self.pSaltos.append(self.cuads_totales)
    def agregarForCond(self):
        self.agregarOperador('<=')
        self.agregarExp(['<='])
        self.agregarIf()
    def agregarFor(self):
        uno = self.guardarCte(1,'int')
        self.pVars.append(self.pVars[-1])
        self.pVars.append(self.pVars[-1])
        self.agregarCte(uno)
        self.agregarOperador('=')
        self.agregarOperador('+')
        self.agregarExp(['+'])
        self.agregarAsignacion()
        self.terminarLoop()
        self.pVars.pop()
    def agregarFunc(self,func):
        self.pFuncs.append(func)
    def agregarWhile(self):
        self.pSaltos.append(self.cuads_totales)
    def terminarLoop(self):
        fin = self.pSaltos.pop()
        prin = self.pSaltos.pop()
        self.agregarCuad(('GoTo',None,None,prin))
        self.completarCuad(fin,self.cuads_totales)
    def agregarMain(self):
        self.agregarCuad(('GoTo',None,None,None))
        self.pSaltos.append(0)
    def completarMain(self):
        salto = self.pSaltos.pop()
        self.completarCuad(salto,self.cuads_totales)
    def agregarFinFunc(self):
        if self.cont_return == 0 and self.dir_func.getRetornoFunc() != 'void':
            raise Exception("A esta funcion le hace falta un return!")

        self.dir_func.setEra(self.vDir.getEra())
        self.resetContadores()
        self.agregarCuad(('EndFunc', None, None, None))
    def resetContadores(self):
        self.cont_return = 0
        self.cont_temporales = 0
        self.vDir.resetVarLocal()
    def agregarReturn(self):
        var = self.pVars.pop()
        tipo_retorno = self.dir_func.getRetornoFunc()

        if self.dir_func.funcActual == self.dir_func.funcGlobal:
            raise Exception("No se puede tener retorno en main!")

        if tipo_retorno == "void":
            raise Exception("No se puede usar return en funciones void!")

        if var.tipo != tipo_retorno:
            raise Exception(f"Type mismatch! -> {var.tipo} != {tipo_retorno}")

        if self.dir_func.getRetornoDirFunc() is None:
            self.dir_func.setRetornoDirFunc(self.vDir.guardarEspacio(self.dir_func.funcActual, tipo_retorno))
        
        return_addr = self.dir_func.getRetornoDirFunc()
        
        self.agregarCuad(('=', var.dir, None, return_addr))
        self.agregarCuad(('RETURN', None, None, return_addr))
        self.cont_return += 1
    def agregarEra(self,func):
        self.agregarCuad(('ERA', None, None, func))
    def getTopFunc(self):
        return self.pFuncs[-1]
    def agregarParam(self,param,count):
        var = self.pVars.pop()
        if var.tipo != param[1]:
            raise Exception(f'Type missmatch! {var.tipo} != {param[1]}')
        
        self.agregarCuad(('PARAM', var.dir, param[0], count))
    def agregarFuncSub(self,func,start):
        self.agregarCuad(('GoSub',None,None,start))
    def agregarRetFunc(self):
        func = self.pFuncs.pop()
        ret_tipo = self.dir_func.getReturnOfFunc(func)
        if ret_tipo == 'void':
            raise Exception(f'Funcion void no se puede usar en expresion! -> {func}')
        res = self.vDir.guardarEspacio('temp',ret_tipo)

        self.agregarCuad(('=>',None,None,res))
        self.agregarTemporal(ret_tipo,res)
        self.cont_temporales +=1
    def agregarEspFunc(self):
        func = self.pFuncs.pop()
        var = self.pVars.pop()
        print(var.tipo)
        if func == 'Line' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'Point' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'Circle' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'ArcUp' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'ArcDown' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'SetX' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'SetY' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'Right' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'Left' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'PenSize' and var.tipo != 'int':
            raise Exception(f'La funcion {func} debe llevar como parametro una variable int,se encontro {var.tipo}')
        if func == 'Color' :
            var2 = self.pVars.pop()
            var3 = self.pVars.pop()
            if var.tipo != 'int' or var2.tipo != 'int' or var3.tipo != 'int':
                raise Exception(f'Una de los parametros de la funcion {func} no es int')
            else:
                self.agregarCuad((func,var3.dir,var2.dir,var.dir))
                return

        self.agregarCuad((func,None,None,var.dir))
    def agregarFinPro(self):
        self.agregarCuad(('FIN',None,None,None))
    def build(self):
        archivo = f'{config.nombre_archivo}.o'

        f = open(archivo,'w')

        f.write('=== RANGOS ===\n')
        for i in self.vDir.getRangos():
            f.write(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}\n')
        f.write('=== FIN RANGOS ===\n')

        f.write('=== CONSTANTES ===\n')
        for cte in self.dir_func.tablaCte.values():
            f.write(f'{cte.valor}\t{cte.tipo}\t{cte.vDir}\n')
        f.write('=== FIN CONSTANTES ===\n')

        f.write('=== ERAS ===\n')
        for func in self.dir_func.diccionario:
            if func == 'main':
                continue
            era = self.dir_func.getEra(func)
            locales = '\t'.join([str(x) for x in era[0]])
            temporales = '\t'.join([str(x) for x in era[1]])
            f.write(f'{func}\t{locales}\t{temporales}\n')
        f.write('=== FIN ERAS ===\n')

        f.write('=== CUADS ===\n')
        for cuad in self.cuads:
            f.write(f'{cuad[0]}\t{cuad[1]}\t{cuad[2]}\t{cuad[3]}\n')
        f.write('=== FIN CUADS ===\n')
    def imprimirCuads(self):
        i = 0
        for c in self.cuads:
            print(f'{i}:\t{c[0]}\t{c[1]}\t{c[2]}\t{c[3]}')
            i += 1
    
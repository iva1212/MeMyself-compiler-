from collections import deque, defaultdict
from turtle import *
import re
import tkinter 
class Var:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo

    def getActualValue(self):
        if self.tipo == 'int':       # regresa Int
            return int(self.valor)
        elif self.tipo == 'float':   # Regresa Float
            return float(self.valor)
        else:                           
            return self.valor
class meVM:
    def __init__(self,file):

        # hacer una pila con el archivo
        lineas = deque(file.split('\n'))
        if lineas.popleft() != '=== RANGOS ===':
            self._error()
        
        self.varGlobales = (self._stringsToNumbers(lineas.popleft().split('\t')))
        self.varLocales = (self._stringsToNumbers(lineas.popleft().split('\t')))
        self.varTemp = (self._stringsToNumbers(lineas.popleft().split('\t')))
        self.varCte = (self._stringsToNumbers(lineas.popleft().split('\t')))
        
        if lineas.popleft() != '=== FIN RANGOS ===':
            self._error()

        self.memGlobal = [None] * (self.varGlobales[4] - self.varGlobales[0])
        self.memLocal = [[None] * (self.varLocales[4] - self.varLocales[0])]
        self.memTemporal = [[None] * (self.varTemp[4] - self.varTemp[0])]
        self.memCtes = [None] * (self.varCte[4] - self.varCte[0])
        
        self.offsetLocal = [[0, 0, 0, 0]]
        self.offsetTemporal = [[0, 0, 0, 0]]

        if lineas.popleft() != '=== CONSTANTES ===':
            self._error()
        
        while True:
            linea = lineas.popleft()
            if linea == '=== FIN CONSTANTES ===':
                break
            datos = linea.split('\t')

            dir = int(datos[2]) - self.varCte[0]
            self.memCtes[dir] = Var(datos[0],datos[1])
            print(('Init', f'{datos[0]} -> ({datos[2]})'))
        self.eras = dict()
        if lineas.popleft() != '=== ERAS ===':
            self._error()
        while True:
            linea = lineas.popleft()

            if linea == '=== FIN ERAS ===':
                break

            datos = linea.split('\t')
            func = datos[0]
            local = self._stringsToNumbers(datos[1:5])
            temp = self._stringsToNumbers(datos[5:9])
            self.eras[func] = [local, temp]

            print('Init', f'ERA - {func} -> {[local, temp]}')
        self.cuads = deque()
        if lineas.popleft() != '=== CUADS ===':
            self._error()
        while True:
            linea = lineas.popleft()

            if linea == '=== FIN CUADS ===':
                break

            self.cuads.append(linea.split('\t'))
        self.pLlamadas = deque()
        self.pReturno = deque()
        self.pParams = deque()
        self.auxLocal = [None]
        self.auxTemp = [None]
    def _error(self):
         raise Exception('Error en el archivo objeto')
    def _stringsToNumbers(self, arr):
        return [int(i) for i in arr]
    def getIndexLocal(self, dir, rango, offset):
        dir = int(dir)
        i = -1
        for r in rango[:-1]:
            if dir >= r:
                i += 1
                ret = dir - r
            if dir < r:
                break
        return ret + offset[i]

    def getTipoDir(self,dir,rangos):
        dir = int(dir)
        if dir < rangos[1]:
            return 'int'
        elif dir < rangos[2]:
            return 'float'
        elif dir < rangos[3]:
            return 'char'
        else:
            return 'bool'
    def getTipo(self,dir):
        dir = int(dir)
        if dir < self.varGlobales[0] or dir >= self.varTemp[4]:
            raise Exception(f'Direccion fuera de memoria {dir}')

        if dir < self.varGlobales[1]:
            return 'int'
        elif dir < self.varGlobales[2]:
            return 'float'
        elif dir < self.varGlobales[3]:
            return 'char'
        elif dir < self.varGlobales[4]:
            return 'bool'
        elif dir < self.varLocales[1]:
            return 'int'
        elif dir < self.varLocales[2]:
            return 'float'
        elif dir < self.varLocales[3]:
            return 'char'
        elif dir < self.varLocales[4]:
            return 'bool'
    def getValor(self,dir):
        dir = int(dir)
        try:
            if dir < self.varGlobales[0] or dir >= self.varCte[4]:
                self._error()
            elif dir < self.varGlobales[4]:
                return self.memGlobal[dir - self.varGlobales[0]]
            elif dir < self.varLocales[4]:
                memDir = None
                if len(self.memLocal) == 1:
                    memDir = dir - self.varLocales[0]
                else:
                    memDir = self.getIndexLocal(dir, self.varLocales, self.offsetLocal[-1])
                return self.memLocal[-1][memDir]
            elif dir < self.varTemp[4]:
                memDir = None
                if len(self.memTemporal) == 1:
                    memDir = dir - self.varTemp[0]
                else:
                    memDir = self.getIndexLocal(dir, self.varTemp, self.offsetTemporal[-1])
                return self.memTemporal[-1][memDir]
            else:
                return self.memCtes[dir - self.varCte[0]]
        except:
            raise Exception(f'Var no asignada en memoria -> {dir}')
    def setValor(self,valor,dir):
        dir = int(dir)
        if dir < self.varGlobales[0] or dir >= self.varCte[4]:
            self._error()
        elif dir < self.varGlobales[4]:
            memDir = dir - self.varGlobales[0]
            self.memGlobal[memDir] = Var(valor, self.getTipoDir(dir,self.varGlobales))
        elif dir < self.varLocales[4]:
            memDir = None
            if len(self.memLocal) == 1:
                memDir = dir - self.varLocales[0]
            else:
                memDir = self.getIndexLocal(dir, self.varLocales, self.offsetLocal[-1])
            self.memLocal[-1][memDir] = Var(valor, self.getTipoDir(dir, self.varLocales))
        elif dir < self.varTemp[4]:
            memDir = None
            if len(self.memTemporal) == 1:
                memDir = dir - self.varTemp[0]
            else:
                memDir = self.getIndexLocal(dir, self.varTemp, self.offsetTemporal[-1])
            self.memTemporal[-1][memDir] = Var(valor, self.getTipoDir(dir, self.varTemp))
        else:
            memDir = dir - self.varCte[0]
            self.memCtes[memDir] = Var(valor,self.getTipoDir(dir,self.varCte))
    def checkAgregar(self,valor,dir,tipo,wn):
        val=None
        if tipo == 'int':
            val = int(valor)
        elif tipo == 'float':
            val = float(valor)
        elif tipo == 'char':
            val = valor[0]
        self.setValor(val,dir)
        wn.destroy()
    def agregarEra(self,func):
        func_eras = self.eras[func]
        self.auxLocal = [None] * sum(func_eras[0])
        era_local = [0]
        for i in func_eras[0][:-1]:
            era_local.append(era_local[-1] + i)
        self.offsetLocal.append(era_local)
        self.auxTemp = [None] * sum(func_eras[1])
        print(self.auxTemp)
        era_temp = [0]
        for i in func_eras[1][:-1]:
            era_temp.append(era_temp[-1] + i)
        self.offsetTemporal.append(era_temp)
        self.pParams.append([])
    def popFuncion(self):
        self.memLocal.pop()
        self.memTemporal.pop()
        self.offsetLocal.pop()
        self.offsetTemporal.pop()
        return self.pLlamadas.pop()
    def correr(self):
        #Setup del gui de la compilacion.

        wn = Screen()
        wn.setup(width = 800,height = 600, startx = 600 , starty= 20)
        bob = Turtle() 
        wn.colormode(255)
        consola = tkinter.Tk()
        consola.geometry("800x200+600+680")
        consola.title("Consola")
        txt = tkinter.Text(consola,height = 200,width = 800)
        scroll = tkinter.Scrollbar(consola) 
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        txt.pack(side=tkinter.LEFT, fill=tkinter.Y)
        scroll.config(command=txt.yview)
        txt.config(yscrollcommand=scroll.set)       

        cont = 0
        while True:
            cuad = self.cuads[cont]
            op = cuad[0]
            
            #LA GRAN LISTA DE OPERADORES
            # operaciones con turtle
            if op == 'Line':
               val = self.getValor(cuad[3]).getActualValue()
               bob.forward(val)
            elif op == 'SetX':
               val = self.getValor(cuad[3]).getActualValue() 
               bob.setx(val)
            elif op == 'SetY':
               val = self.getValor(cuad[3]).getActualValue() 
               bob.sety(val)
            elif op == 'PenUp':
                bob.penup()
            elif op == 'PenDown':
                bob.pendown()
            elif op == 'PenSize':
                val = self.getValor(cuad[3]).getActualValue()
                bob.pensize(val)
            elif op == 'Right':
                val = self.getValor(cuad[3]).getActualValue()
                bob.right(val)
            elif op == 'Left':
                val = self.getValor(cuad[3]).getActualValue()
                bob.left(val)
            elif op == 'Color':
                val1 = self.getValor(cuad[1]).getActualValue()
                val2 = self.getValor(cuad[2]).getActualValue()
                val3 = self.getValor(cuad[3]).getActualValue()

                bob.color(val1,val2,val3)
            elif op == 'Circle':
                val = self.getValor(cuad[3]).getActualValue()
                bob.circle(val)
            elif op == 'ArcDown':
                val = self.getValor(cuad[3]).getActualValue()
                bob.circle(val,180)
            elif op == 'ArcUp':
                val = self.getValor(cuad[3]).getActualValue()
                bob.circle(val,-180)
            elif op == 'Point':
                val = self.getValor(cuad[3]).getActualValue()
                bob.dot(val)
            elif op == 'Clear':
                bob.clear()

            # operaciones basicas
            elif op in ['+', '-', '/', '*', '==', '!=', '<', '<=', '>', '>=', '&', '|']:
                izq = self.getValor(cuad[1]).getActualValue()
                der = self.getValor(cuad[2]).getActualValue()

                res = None
                if op == '&':
                    res= eval(f'{izq} and {der}')
                elif op == '|':
                    res = eval(f'{izq} or {der}')
                else:
                    res = eval(f'{izq} {op} {der}')

                self.setValor(res, cuad[3])
            elif op =='=':
                valor = self.getValor(cuad[1]).getActualValue()
                self.setValor(valor,cuad[3])
            elif op == 'GoTo':
                cont = int(cuad[3])
                continue
            elif op == 'GoToF':
                boolean = self.getValor(cuad[1]).getActualValue()
                
                if not boolean:
                    cont = int(cuad[3]) - 1
                else:
                    print("No Jump")
            elif op == 'WRITE':
                valor = cuad[3]
                if re.match(r'\".*\"',valor):
                    string = valor[1:-1]
                    txt.insert(tkinter.INSERT,string+'\n')
                else:
                    string = str(self.getValor(valor).getActualValue())
                    txt.insert(tkinter.INSERT,string+'\n')
            elif op == 'READ':
                dir = cuad[3]
                tipo = self.getTipo(dir)
                pop = tkinter.Toplevel(consola)
                pop.title("input")
                pop.geometry("200x100+700+700")
                pop.attributes("-topmost",True)
                l = tkinter.Label(pop,text=cuad[1])
                e1 = tkinter.Entry(pop)
                btn = tkinter.Button(pop,text="Enter",command=lambda: self.checkAgregar(e1.get(),dir,tipo,pop))
                l.pack()
                e1.pack()
                btn.pack()
                consola.wait_window(pop)
            elif op == 'ERA':
                self.agregarEra(cuad[3])
            elif op == 'PARAM':
                param = self.getValor(cuad[1]).getActualValue()
                self.pParams[-1].append((param,cuad[2]))
            elif op == 'RETURN':
                ret = self.getValor(cuad[3]).getActualValue()
                self.pReturno.append(ret)
                cont = self.popFuncion()

            elif op == 'GoSub':
                self.pLlamadas.append(cont)
                self.memLocal.append(self.auxLocal)
                self.memTemporal.append(self.auxTemp)

                params = self.pParams.pop()
                for i in params:
                    self.setValor(i[0],i[1])
                
                cont = int(cuad[3])
                print(cont)
                continue
            elif op == '=>':
                ret = self.pReturno.pop()
                self.setValor(ret,cuad[3])
            elif op == 'EndFunc':
                cont = self.popFuncion()
            elif op == 'FIN':
                print("FIN DEL PROGRAMA")
                break
            cont +=1

        #Se termina de modificar el gui
        bob.hideturtle()
        done()
        consola.mainloop()

        

def me(file):
    vm = meVM(file)
    vm.correr()

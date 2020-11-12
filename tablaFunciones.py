from tablaVariables import tablaVariables
class Constante():
    def __init__(self, valor, tipo, vDir):
        self.valor = valor
        self.tipo = tipo
        self.vDir = vDir
class tablaFunciones(object):
    def __init__(self):
        self.diccionario = {}
        self.tablaCte = dict()
        self.funcGlobal = None
        self.funcActual = None
        self.count_param = 0


    def agregarFuncion(self, name, returnType):
        
        if not self.funcionExiste(name):
            self.diccionario[name] = {
                "tipoRetorno": returnType,
                "startCuad": None,
                "dirRetorno" : None,
                "tablaVariables": tablaVariables(),
                "parametros": [],
                "era" : []
            }
            return "OK"
        else:
            if name == "main":
                return "main"
            else:
                return name

    def funcionExiste(self, name):
        if name in self.diccionario:
            return True
        else:
            return False
    def agregarVariables(self, listaVars, tipo):
        for variable in listaVars:
            if not self.diccionario[self.funcActual]["tablaVariables"].varExiste(variable[0]):
                self.diccionario[self.funcActual]["tablaVariables"].agregarVariable(variable[0],variable[1],tipo)
            else: 
                return variable
        return "OK"
    def agregarParam(self,vDir,tipo):
        self.diccionario[self.funcActual]["parametros"].append((vDir,tipo))
    def agregarCte(self,valor,tipo,vDir):
        self.tablaCte[(valor,tipo)] = Constante(valor,tipo,vDir)
    def agregarVariable(self,nombre,vDir,tipo):
        if not self.diccionario[self.funcActual]["tablaVariables"].varExiste(nombre):
            self.diccionario[self.funcActual]["tablaVariables"].agregarVariable(nombre,vDir,tipo)
    def buscarVariable(self, name, nombreFuncion):
        resultado = self.diccionario[nombreFuncion]["tablaVariables"].buscarVariable(name)
        if resultado == "ERROR":
            resultado = self.diccionario[self.funcGlobal]["tablaVariables"].buscarVariable(name)
            if resultado == "ERROR":
                return "ERROR"
            else:
                return resultado
        else:
            return resultado
    def getCte(self,valor,tipo):
        return self.tablaCte[(valor,tipo)]
    def setFuncGlobal(self):
        self.funcGlobal = self.funcActual
    def setFuncActual(self,funcActual):
        self.funcActual = funcActual
    def existeCte(self,valor,tipo):
        return (valor,tipo) in self.tablaCte
    def existeVar(self,nombre,nombreFuncion):
        if self.diccionario[nombreFuncion]["tablaVariables"].varExiste(nombre):
            return True
        else:
            return False
    def setEra(self,era):
        self.diccionario[self.funcActual]["era"] = era
    def getEra(self,func):
        return self.diccionario[func]["era"]
    def incrementarParam(self):
        self.count_param += 1
    def getRetornoFunc(self):
        return self.diccionario[self.funcActual]["tipoRetorno"]
    def getReturnOfFunc(self,func):
        return self.diccionario[func]["tipoRetorno"]
    def getRetornoDirFunc(self):
        return self.diccionario[self.funcActual]["dirRetorno"]
    def setRetornoDirFunc(self,vDir):
        self.diccionario[self.funcActual]["dirRetorno"] = vDir
    def getParam(self,func):
        return self.diccionario[func]["parametros"][self.count_param]
    def verificarParams(self,func):
        return (self.count_param == len(self.diccionario[func]["parametros"]))
    def resetParamCount(self):
        self.count_param = 0
    def printFunciones(self):
        for funciones in self.diccionario:
            print(funciones)
    def setStartCuad(self,cu):
        self.diccionario[self.funcActual]["startCuad"] = cu
    def getStartCuad(self,func):
        return self.diccionario[func]["startCuad"]
    def printVariables(self):
        for funcion in self.diccionario:
            print(funcion)
            self.diccionario[funcion]["tablaVariables"].printVariables()
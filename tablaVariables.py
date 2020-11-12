class tablaVariables(object):
    def __init__(self):
        self.diccionario = {}

    def agregarVariable(self, nombre, vDir,tipoVar):
        self.diccionario[nombre] = {
            "id_var"  : nombre,
            "tipo": tipoVar,
            "vDir": vDir
        }

    def varExiste(self, nombre):
        if nombre in self.diccionario:
            return True
        else:
            return False

    def printVariables(self):
        for vars in self.diccionario:
            print("NombreVar:", vars, "Tipo:", self.diccionario[vars]["tipo"],"vDir :",self.diccionario[vars]["vDir"])

    def buscarVariable(self, nombre):
        if self.varExiste(nombre):
            return self.diccionario[nombre]
        else:
            return "ERROR"
        
    

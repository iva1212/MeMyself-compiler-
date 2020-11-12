class cuboSemantico:
    def __init__(self):
        self.cuboSem = {
            "int" : {
                "int" : {
                    "+" : "int",
                    "-" : "int",
                    "*" : "int",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "int"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" : "error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "float" : {
                "int" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "float"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    "|" : "error",
                    "&" : "error",
                    "=" : "float"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "char" : {
                "int" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "float" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "char"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                }
            },
            "bool" : {
                "int" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error" 
                },
                "float" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "char" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "error",
                    "!=" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "error",
                    "&" : "error",
                    "=" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "==" : "bool",
                    "!=" : "bool",
                    ">=" : "error",
                    "<=" : "error",
                    ">" : "error",
                    "<" :"error",
                    "|" : "bool",
                    "&" : "bool",
                    "=" : "error"
                }
            }
        }
        self.tipoOp1Actual=""
        self.tipoOp2Actual=""
        self.operacionActual=""

    def obtenerSem(self, op1, op2, operacion):
        return self.cuboSem[op1][op2][operacion]
    def setTipoOp1Actual(self,op1):
        self.tipoOp1Actual = op1
    def setTipoOp2Actual(self,op2):
        self.tipoOp2Actual = op2
    def setOperacionActual(self,operacion):
        self.operacionActual = operacion
    def clearOp(self):
        self.tipoOp1Actual=""
        self.tipoOp2Actual=""
        self.operacionActual=""
    def getResultado(self):
        return  self.cuboSem[self.tipoOp1Actual][self.tipoOp2Actual][self.operacionActual]


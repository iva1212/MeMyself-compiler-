class manejadorDirecciones:
  def __init__(self):
      # ( int  float  char  bool )
      self.varGlobales = (1000, 4000, 7000, 8000, 9000)
      self.varLocales =  (9000, 13000, 17000, 18500, 20000)
      self.varTemp =   (20000, 24000, 28000, 29500, 31000)
      self.varCte =    (31000, 34000, 37000, 37500, 38000)

      self.globalCounter = [0, 0, 0, 0]
      self.localCounter = [0, 0, 0, 0]
      self.tempCounter = [0, 0, 0, 0]
      self.cteCounter = [0, 0, 0, 0]

      self.contador_Total = 0

    # Se separa espacio para la variable
  def guardarEspacio(self, scope, tipoVar):
  
    tipo = None
    if tipoVar == 'int':
      tipo = 0
    elif tipoVar == 'float':
      tipo = 1
    elif tipoVar == 'char':
      tipo = 2
    elif tipoVar == 'bool':
      tipo = 3

   
    self.contador_Total += 1

    if scope == 'global':   # Global
      if self.varGlobales[tipo] + self.globalCounter[tipo] + 1 >= self.varGlobales[tipo + 1] - 1:
        raise Exception(f"Fuera de memoria! {tipoVar} in {scope}")
      self.globalCounter[tipo] += 1
      return self.varGlobales[tipo] + self.globalCounter[tipo] - 1
    elif scope == 'cte':    # Constantes
      if self.varCte[tipo] + self.cteCounter[tipo] + 1 >= self.varCte[tipo + 1] - 1:
        raise Exception(f"Fuera de memoria! {tipoVar} in {scope}")
      self.cteCounter[tipo] += 1
      return self.varCte[tipo] + self.cteCounter[tipo] - 1
    elif scope == 'temp':   # Temp
      if self.varTemp[tipo] + self.tempCounter[tipo] + 1 >= self.varTemp[tipo + 1] - 1:
        raise Exception(f"Fuera de memoria! {tipoVar} in {scope}")
      self.tempCounter[tipo] += 1
      return self.varTemp[tipo] + self.tempCounter[tipo] - 1
    else:                   # Local 
      if self.varLocales[tipo] + self.localCounter[tipo] + 1 >= self.varLocales[tipo + 1] - 1:
        raise Exception(f"Fuera de memoria! {tipoVar} in {scope}")
      self.localCounter[tipo] += 1
      return self.varLocales[tipo] + self.localCounter[tipo] - 1

    raise Exception(f'Invalido -> {tipoVar}, {scope}')
  def resetVarLocal(self):
    self.localCounter = [0,0,0,0]
    self.tempCounter = [0,0,0,0]
  def getRangos(self):
    return [self.varGlobales, self.varLocales, self.varTemp, self.varCte]
  def getEra(self):
    return [self.localCounter, self.tempCounter]
  
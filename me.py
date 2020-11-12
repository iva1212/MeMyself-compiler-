import config
from virtualMachine import me


data = ''

try:
  with open(f'{config.nombre_archivo}.o') as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception(f'{config.nombre_archivo}.o no existe!')

me(data)
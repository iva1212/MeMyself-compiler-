import config
import argparse
from os import path
from ply import lex, yacc
from virtualMachine import me

cli = argparse.ArgumentParser(description='ME Compiler')
cli.add_argument('file', help='Specify a file to run through')
args = cli.parse_args()

filepath = path.splitext(args.file)
config.nombre_archivo = filepath[0]

exec(open("./parser.py").read())


data = ''
try:
  with open(f'{config.nombre_archivo}.o') as f:
    for line in f:
      data += line
except FileNotFoundError:
  raise Exception(f'{config.nombre_archivo}.o no existe!')

me(data)
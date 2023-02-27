# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa


# Importar clases
from symbol import Symbol
from toPostfix import toPostfix
from stack import Stack

# Expresión regular sobre la que se hará el autómata
regex = "ab*(c|d)e"
stack = Stack()
temp = Stack()

# Convertir cada símbolo de la regex en un objeto
[stack.push(Symbol(obj)) for obj in regex]
toPostfix(stack, temp)



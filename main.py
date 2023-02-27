# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from automata import automata
from validations import addConcatenations
from toPostfix import infix_to_postfix
from symbol import Symbol
from node import Node
from stack import Stack, toStack, toList

# Expresión regular sobre la que se hará el autómata
regex = "(a|b).(c|d)?.e"

# Expresión regular infix: a|b.c
# Expresión regular postfix: abc.|
# Expresión regular infix: (a|b).c
# Expresión regular postfix: ab|.c.
# Expresión regular infix: a.(b|c)+
# Expresión regular postfix: abc|+.
# Expresión regular infix: (a|b).(c|d)?.e
# Expresión regular postfix: ab|cd|?.e.
# Expresión regular infix: a+bc?
# Expresión regular postfix: abc+?

regex = infix_to_postfix(regex)
print(regex)
regex = [Symbol(i) for i in regex]
stack = toStack(regex)
print(stack.item)

# Create nodes
operandos = Stack()

while stack.size() > 0:
    val = stack.pop()
    # definir casos
    print(val.value, operandos.size())
    if val.value not in "+|*?.":
        operandos.push(val)

    elif val.value in "|.":
        parent = val
        left = operandos.pop()
        right = operandos.pop()
        # Crear nodo
        operandos.push(Node(parent=parent, left=left, right=right))

    elif val.value in "*+?":
        parent = val
        left = operandos.pop()
        operandos.push(Node(parent = parent, left = left))

print(operandos.item)
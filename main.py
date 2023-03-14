# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from toPostfix import infix_to_postfix, alphabet
from symbol import Symbol
from node import Node
from stack import Stack, toStack, toList

# Expresión regular sobre la que se hará el autómata
regex = "(a+).b.(c?)"
# Obtener alfabeto
alphabet = alphabet(regex)

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

regex = infix_to_postfix(regex, alphabet)
print(regex)
regex = [Symbol(i) for i in regex]
stack = toStack(regex)

# Create nodes
operandos = Stack()

# árbol y construcción de AFN
while stack.size() > 0:
    val = stack.pop()
    # definir casos
    if val.value not in "+|*?.":
        nodo = Node(parent=val)
        operandos.push(nodo)

    elif val.value in "|.":
        parent = val
        left = operandos.pop()
        right = operandos.pop()
        # Crear nodo
        nodo = Node(parent=parent, left=left, right=right)
        operandos.push(nodo)

    elif val.value == "?":
        # Crear nodo para ε
        right = Symbol("ε")
        right = Node(parent=right)

        parent = Symbol("|")
        left = operandos.pop()
        nodo = Node(parent=parent, left=left, right=right)
        operandos.push(nodo)

    elif val.value == "+":
        # Crear primero nodo kleene
        parent = Symbol("*")
        left = operandos.pop()
        nodoKleene = Node(parent = parent, left = left)

        # Crear concatenación
        parent = Symbol(".")
        right = nodoKleene
        nodo = Node(parent=parent, left=left, right=right)
        operandos.push(nodo)

    elif val.value in "*":
        parent = val
        left = operandos.pop()
        nodo = Node(parent = parent, left = left)
        operandos.push(nodo)

res = operandos.item[0]
tree = res.printNode()
print('arbol: ', tree)
thompsonAFN = res.thompsonAutomataAFN
thompsonAFN.to_graphviz()
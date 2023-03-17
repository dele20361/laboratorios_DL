# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from toPostfix import infix_to_postfix, alphabetF
from symbol import Symbol
from node import Node
from stack import Stack, toStack

# Expresión regular sobre la que se hará el autómata
regex = input("Expresión regular a generar: ") or "(a*)b"
# Obtener alfabeto
alphabet = alphabetF(regex)

regex = infix_to_postfix(regex)
print(regex)
regex = [Symbol(i) for i in regex]
operandos = Stack()

# # Pruebas
# (a*|b*)c
# (b|b)*abb(a|b)*
# (a|ε)b(a+)c?
# (a|b)*a(a|b)(a|b)
# b*ab?
# b+abc+
# ab*ab*
# 0(0|1)*0
# ((ε|0)1*)*
# (0|1)*0(0|1)(0|1)
# (00)*(11)*

# árbol y construcción de AFN
for val in regex:
    # definir casos
    if val.value not in "+|*?.":
        nodo = Node(parent=val)
        operandos.push(nodo)

    elif val.value in "|.":
        parent = val
        right = operandos.pop()
        left = operandos.pop()
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
        right = operandos.pop()
        nodoKleene = Node(parent = parent, left = left)

        # Crear concatenación
        parent = Symbol(".")
        left = nodoKleene
        nodo = Node(parent=parent, left=left, right=right)
        operandos.push(nodo)

    elif val.value in "*":
        parent = val
        left = operandos.pop()
        nodo = Node(parent = parent, left = left)
        operandos.push(nodo)

res = operandos.pop()
tree = res.printNode()
print('arbol: ', tree)
thompsonAFN = res.thompsonAutomataAFN
thompsonAFN.to_graphviz(filename='AFN_thompson')
AFDsubset = thompsonAFN.to_AFD()
AFDsubset.to_graphviz(filename = 'AFD_subset')
# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio C

from types import NoneType
from symbol import Symbol
from stack import Stack
from node import Node

def checkParenthesis(cadena):
    pila = []
    for caracter in cadena:
        if caracter == "(" or caracter == "[":
            pila.append(caracter)
        elif caracter == ")":
            if len(pila) == 0 or pila[-1] != "(":
                return False
            pila.pop()
        elif caracter == "]":
            if len(pila) == 0 or pila[-1] != "[":
                return False
            pila.pop()
    return len(pila) == 0

def deep(right, alphabetNumbers, number):
    pending = Stack()
    node = right.deepcopy_node(right) if not isinstance(right, NoneType) else None
    pending.push((node, '')) if not isinstance(right, NoneType) else None

    prevNode = None

    while not pending.isEmpty():

        new = pending.pop()
        nodeTemp = new[0]
        side = new[1]

        if isinstance(nodeTemp.parent, Symbol) and nodeTemp.parent.notOperator():
            # Ver de qué lado se está evaluando
            # Crear nuevo simbolo
            newParent = Symbol(nodeTemp.parent.value, number=number)
            newNode = Node(parent=newParent)
            number = checkNumber(newNode, number)
            alphabetNumbers[newNode.parent.number] = newParent

            if side == 'L':
                prevNode.left = newNode
            elif side == 'R':
                prevNode.right = newNode

        else:
            # Cambiar el nodo parent para el valor de la izquierda o para el de la izquierda
            # Ver si tiene un left y un right, si tiene uno pushear el right a un stack para visitarlo después.
            if nodeTemp.left is not None and nodeTemp.right is not None:
                # Pushear a stack
                pending.push((nodeTemp.right, 'R')) # Push de nodos
                pending.push((nodeTemp.left, 'L'))

            elif nodeTemp.left is not None:
                pending.push((nodeTemp.left, 'L')) # Push de nodo

            prevNode = nodeTemp

    right = node
    return right

def checkNumber(node, number):
    parent = node.parent
    if parent.notOperator() and parent.value != 'ε':
        number = number + 1
        parent.changeNumber(number)
    
    return number

def convertToSymbol(regex):
    res = []
    i = 0
    while i < len(regex):
        # Ver si es \t, \n, etc
        if regex[i] == "\\":
            if (i+1) < len(regex):
                temp = Symbol(str('\\'+regex[i+1]))
                res.append(temp)
                i = i + 2
            else:
                print("@ Error! Después de \\ se espera un caracter.")
                i = i + 1

        # Ver si es un caracter especial
        elif ((i+2) < len(regex)) and (regex[i] == "'") and (regex[i+1] in "+.*?|") and regex[i+2] == "'":
            temp = Symbol(regex[i+1], notOp=True)
            res.append(temp)
            i = i + 3

        else:
            res.append(Symbol(regex[i]))
            i = i + 1

    return res

import copy
from AFD import AFD
from toPostfix import infix_to_postfix, alphabetF
from types import NoneType
from symbol import Symbol
from symbol import Symbol
from validations import *
from stack import Stack
from node import Node


class Tree:

    def __init__(self, regex, direct, number, tokenName=None) -> None:
        """
            Árbol sintáctico.
        """
        self.regex = regex
        self.treeTuple = ()
        self.direct = direct
        self.hashtagNumber = 0
        self.numberGlobal = number
        self.tokenName = tokenName
        self.alphabetNumbers = {}
        self.tree = ()
        self.alphabet = alphabetF(self.regex)
        self.createTree()


    def createTree(self):
        """
            Creación de árbol con método directo.
        """
        # Obtener alfabeto y convertir a postfix
        self.regex = infix_to_postfix(self.regex)
        # Convertir a objeto symbol
        self.regex = convertToSymbol(self.regex)

        # Construcción del árbol
        operandos = Stack()

        for val in self.regex:
            # definir casos
            if val.value not in "+|*?." or val.notOp == True:
                self.numberGlobal = self.numberGlobal + 1
                val.changeNumber(number=self.numberGlobal)
                nodo = Node(parent=val, direct=self.direct)
                self.alphabetNumbers[nodo.parent.number] = val
                operandos.push(nodo)

            elif val.value in "|." and val.notOp == False:
                parent = val
                right = operandos.pop()
                left = operandos.pop()
                if isinstance(left, NoneType) or isinstance(right, NoneType):
                    print('@ Error en "'+ val.value + '"!. Para este operador se requieren 2 operandos.')

                # Crear nodo
                nodo = Node(parent=parent, left=left, right=right, direct=self.direct)
                operandos.push(nodo)

            elif val.value == "?" and val.notOp == False:
                # Crear nodo para ε
                right = Symbol("ε")
                right = Node(parent=right, direct=self.direct)
                parent = Symbol("|")
                left = operandos.pop()

                if isinstance(left, NoneType):
                    print('@ Error en "'+ val.value + '"!. Para este operador se requiere 1 operando.')

                nodo = Node(parent=parent, left=left, right=right, direct=self.direct)
                operandos.push(nodo)

            elif val.value == "+" and val.notOp == False:
                # Crear primero nodo kleene
                parent = Symbol("*")
                left = operandos.pop()
                
                if isinstance(left, NoneType):
                    print('@ Error en "'+ val.value + '"!. Para este operador se requiere 1 operando.')

                # Crear concatenación
                parent = Symbol("+")

                nodo = Node(parent=parent, left=left, direct=self.direct)
                operandos.push(nodo)

            elif val.value == "*" and val.notOp == False:
                parent = val
                left = operandos.pop()
                if isinstance(left, NoneType):
                    print('@ Error en "'+ val.value + '"!. Para este operador se requiere 1 operando.')

                nodo = Node(parent = parent, left = left, direct=self.direct)
                operandos.push(nodo)

        res = operandos.pop()

        concat = Symbol('.')
        hashtagSymbol = Symbol('#', number=self.numberGlobal+1)
        hashtag = Node(parent=hashtagSymbol, direct=self.direct)
        self.alphabetNumbers[self.numberGlobal+1] = hashtagSymbol
        self.alphabet.append('#')
        self.hashtagNumber = self.numberGlobal

        # Añadir nodo terminal
        self.tree = Node(parent=concat, left=res, right=hashtag, direct=self.direct)
        self.treeTuple = self.tree.printNode()

        return self.tree
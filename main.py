# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from graphviz import Digraph
from AFD import AFD
from symbol import Symbol
from node import Node
from stack import Stack
from LabC import Lexer
from tree import Tree

# Expresión regular sobre la que se hará el autómata
# regex = input("Expresión regular a generar: ") or "((0|1|2|3|4|5|6|7|8|9)+)('.'((0|1|2|3|4|5|6|7|8|9)+))?('E'('+'|'-')?((0|1|2|3|4|5|6|7|8|9)+))?"
filepath = input(">> Ingrese el path relativo del archivo .yal: ") or "./testsLabC/slr-2.yal"
lexer = Lexer(filepath)
direct = True

tokens = lexer.rules

if direct:

    print("Método directo")
    # cadena = input("Ingrese la cadena a simular: ") or "bab"

    numberGlobal = 0
    final = ''

    trees = Stack()
    for tokenName, tokenValue in tokens.items():
        final = final + tokenValue + '|'
        treeObj = Tree(tokenValue, direct, numberGlobal, tokenName)
        numberGlobal = treeObj.numberGlobal + 1
        trees.push(treeObj.tree) # Push del nodo árbol

    print('> Expresión regular a generar: ', final[:-1])

    # Obtener el árbol sintáctico final
    while len(trees.item) > 1:
        parent = Symbol("|")
        right = trees.pop()
        left = trees.pop()
        if left is None or right is None:
            print('@ Error en "'+ parent.value + '"!. Para este operador se requieren 2 operandos.')

        # Crear nodo
        nodo = Node(parent=parent, left=left, right=right, direct=direct)
        trees.push(nodo)


    # El árbol sintáctico final estará en el único elemento restante del stack
    treeNodeObj = trees.pop()
    tree = treeNodeObj
    treeTuple = tree.printNode()


    # Visualización de árbol
    graph = Digraph()
    tree.add_nodes(graph, treeTuple)
    graph.render('./treeImage/tree', format='png', view=True)

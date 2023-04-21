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


filepath = input(">> Ingrese el path relativo del archivo .yal: ") or "./testsLabC/slr-1.yal"
lexer = Lexer(filepath)
direct = True

tokens = lexer.rules

if direct:

    numberGlobal = 0
    final = ''
    followpos = {}

    trees = Stack()
    for tokenName, tokenValue in tokens.items():
        final = final + tokenValue + '|'
        treeObj = Tree(tokenValue, direct, numberGlobal, tokenName)
        numberGlobal = treeObj.numberGlobal + 1
        trees.push(treeObj.tree) # Push del nodo árbol

    print('> Expresión regular a generar: ', final[:-1], '\n\n')

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

    # Construcción de AFD por método directo
    alphabetNumbers = treeObj.alphabetNumbers
    alphabet = set()
    [alphabet.add(i.value) for i in list(alphabetNumbers.values())]
    hashtagNumber = numberGlobal

    D_states = set()
    D_transitions = {}
    finalStates = set()

    stack = Stack()
    alphabet.remove('#')

    followpos = treeNodeObj.followpos
    completedFollowpos = {}

    # Completar tabla de siguiente posición con símbolos
    for key, value in followpos.items():
        symbol = alphabetNumbers[key].value
        completedFollowpos[key] = {symbol: value}

    completedFollowpos[hashtagNumber] = {}

    primerEstado = treeNodeObj.primeraPosicion()
    stack.push(primerEstado)
    D_states.add(tuple(primerEstado))

    while not stack.isEmpty():
        state = stack.pop()
        state = tuple(state)
        D_transitions[state] = {}

        for char in alphabet:
            newStates = set()
            for p in state:
                if p in alphabetNumbers.keys() and not alphabetNumbers[p].hashtag and char in completedFollowpos[p]:
                    newStates = newStates.union(completedFollowpos[p][char])

            tempState = newStates
            newStates = tuple(newStates)

            if newStates:
                if newStates not in D_states:
                    D_states.add(newStates)
                    stack.push(newStates)

                    terminals = set([hashtagNumber]).intersection(set(tempState))

                    if terminals:
                        finalStates.add(newStates)

                D_transitions[state][char] = newStates

    # Crear AFD
    afdDirecto = AFD(
                    Q = D_states,
                    q_start = tuple(primerEstado),
                    q_end = finalStates,
                    transitions = D_transitions,
                    alphabet = alphabet
                 )
    
    # Imprimir AFD
    afdDirecto.to_graphviz(filename = 'afdDirecto')

## --------------------------------------------------------------------------------

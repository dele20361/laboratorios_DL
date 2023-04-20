# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from graphviz import Digraph
# from AFD import AFD
from symbol import Symbol
from node import Node
from stack import Stack
from LabC import Lexer
from tree import Tree

# Expresión regular sobre la que se hará el autómata
# regex = input("Expresión regular a generar: ") or "((0|1|2|3|4|5|6|7|8|9)+)('.'((0|1|2|3|4|5|6|7|8|9)+))?('E'('+'|'-')?((0|1|2|3|4|5|6|7|8|9)+))?"
filepath = input(">> Ingrese el path relativo del archivo .yal: ") or "./testsLabC/slr-4.yal"
lexer = Lexer(filepath)
direct = True

tokens = lexer.rules

if direct:

    print("\n\nMétodo directo")
    print(tokens)
    # cadena = input("Ingrese la cadena a simular: ") or "bab"
    trees = Stack()
    for tokenName, tokenValue in tokens.items():
        treeObj = Tree(tokenValue, direct, tokenName)
        trees.push(treeObj.tree) # Push del nodo árbol


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

#     # ----------------------------- Construcción directa -----------------------------
#     # Paso 1: Construcción de tabla siguiente posición
#     # # Seleccionar cada uno de los nodos concat y kleene para construir tabla

#     pending = Stack() # Para almacenar los nodos por analizar
#     pending.push(tree) # Paso base
#     siguientePosicion = {}

#     while not pending.isEmpty():

#         nodeTemp = pending.pop()

#         # Siguiente Posición para caso en donde el valor del nodo derecho sea #
#         if isinstance(nodeTemp.right, Node) and isinstance(nodeTemp.right.parent, Symbol) and nodeTemp.right.parent.value == '#':
#             i = nodeTemp.right.parent.number
#             if i not in siguientePosicion.keys():
#                     siguientePosicion[i] = {}
#                     for c in alphabet:
#                         siguientePosicion[i][c] = set()

#         # Siguiente Posición de concatenación
#         if nodeTemp.parent.value == ".":
#             t = nodeTemp.left.ultimaPosicion()
#             for i in t:
#                 getAlphabet = alphabetNumbers[i].value

#                 # Agregar sets vacíos para cada valor del input
#                 if i not in siguientePosicion.keys():
#                     siguientePosicion[i] = {}
#                     for c in alphabet:
#                         siguientePosicion[i][c] = set()

#                 # print(siguientePosicion)
#                 if i in siguientePosicion.keys() and getAlphabet in siguientePosicion[i].keys():
#                     for j in nodeTemp.right.primeraPosicion():
#                         siguientePosicion[i][getAlphabet].add(j)

#         # Siguiente Posición Cerradura de Kleene
#         elif nodeTemp.parent.value == "*":
#             t = nodeTemp.ultimaPosicion()
#             for i in t:

#                 # Agregar sets vacíos para cada valor del input
#                 if i in siguientePosicion.keys():
#                     for c in alphabet:
#                         if c not in siguientePosicion[i].keys():
#                             siguientePosicion[i] = {c: set()}

#                 getAlphabet = alphabetNumbers[i].value
#                 for j in nodeTemp.primeraPosicion():
#                     siguientePosicion[i][getAlphabet].add(j)

#         if nodeTemp.left is not None and nodeTemp.right is not None:
#             # Push a stack
#             pending.push(nodeTemp.right)
#             pending.push(nodeTemp.left)

#         elif nodeTemp.left is not None:
#             pending.push(nodeTemp.left)

#     # Paso 2: Construcción de tabla de transiciones
#     transiciones = {}
#     D_states = set()

#     simboloPrimerEstado = ''
#     primerEstado = ''

#     for key, value in siguientePosicion[1].items():
#         if value != set():
#             simboloPrimerEstado = key, 
#             primerEstado = value

#     states = Stack()
#     states.push(primerEstado)

#     while not states.isEmpty():
#         state = tuple(states.pop())

#         # Por cada valor del alfabeto recorrer la siguiente pos de cada estado state (que es un set)
#         if state not in D_states:
#             D_states.add(state)
#             transiciones[state] = {}
#             for c in alphabet:
#                 transiciones[state].update({c: set()})

#         state = list(state)
#         nextPos = ''
#         for n in state:
#             for c in alphabet:
#                 nextPos = siguientePosicion[n][c]
#                 nextPos = tuple(nextPos)
#                 transiciones[tuple(state)][c].update(nextPos)

#                 # Agregar nuevo estado
#                 if nextPos != "" and nextPos != () and nextPos not in D_states:
#                     states.push(nextPos)

#    # Estados finales
#     finalStates = list(filter(lambda x: hashtagNumber in x, D_states))

#     # Crear AFD
#     afdDirecto = AFD(
#                     Q = D_states,
#                     q_start = primerEstado,
#                     q_end = finalStates,
#                     transitions = transiciones,
#                     alphabet = alphabet
#                  )
    
#     # Imprimir AFD
#     afdDirecto.to_graphviz(filename = 'afdDirecto')

#     # Simular cadena
#     afdDirecto.simulacion(cadena)

    # --------------------------------------------------------------------------------
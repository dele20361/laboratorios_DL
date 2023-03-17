# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from cmath import pi
from graphviz import Digraph
from numpy import sort
from AFD import AFD
from Minimizacion import Minimizacion
from toPostfix import infix_to_postfix, alphabetF
from symbol import Symbol
from node import Node
from stack import Stack, toStack

# Expresión regular sobre la que se hará el autómata
regex = input("Expresión regular a generar: ") or "(b|b)*abb(a|b)*"
# Dependiendo de este valor se realizará el autómata mediante thompson (AFN)
# y subconjuntos (AFD) o se realizará solamente el AFD
res = input("¿Desea el AFD de forma directa? (Y/n) ")
direct = True if res == 'Y' or res == 'y' else False

# Obtener alfabeto
alphabet = alphabetF(regex)

regex = infix_to_postfix(regex)
print(regex)
regex = [Symbol(i) for i in regex]
operandos = Stack()

# # Pruebas
# (b|b)*abb(a|b)*
# b*ab? 

# Construcción del árbol
number = 0 # Para enumeración del árbol sintáctico
hashtagNumber = 0
alphabetNumbers = {}

def checkNumber(node, number):
    parent = node.parent
    if parent.notOperator() and parent.value != 'ε':
        number = number + 1
        parent.changeNumber(number)
    
    return number

for val in regex:
    # definir casos
    if val.value not in "+|*?.":
        number = number + 1
        val.changeNumber(number=number)
        nodo = Node(parent=val, direct=direct)
        alphabetNumbers[nodo.parent.number] = val
        operandos.push(nodo)

    elif val.value in "|.":
        parent = val
        right = operandos.pop()
        left = operandos.pop()

        # Crear nodo
        nodo = Node(parent=parent, left=left, right=right, direct=direct)
        operandos.push(nodo)

    elif val.value == "?":
        # Crear nodo para ε
        right = Symbol("ε")
        right = Node(parent=right, direct=direct)
        parent = Symbol("|")
        left = operandos.pop()

        nodo = Node(parent=parent, left=left, right=right, direct=direct)
        operandos.push(nodo)

    elif val.value == "+":

        # Crear primero nodo kleene
        parent = Symbol("*")
        right = operandos.pop()
        nodoKleene = Node(parent = parent, left = right, direct=direct)
        
        # Cambiar el valor right con la nueva instancia de symbol.
        pending = Stack()
        node = right.deepcopy_node(right)
        pending.push((node, ''))

        prevNode = None

        while not pending.isEmpty():

            new = pending.pop()
            nodeTemp = new[0]
            # print(nodeTemp.printNode())
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

        # Crear concatenación
        parent = Symbol(".")
        left = nodoKleene

        nodo = Node(parent=parent, left=left, right=right, direct=direct)
        operandos.push(nodo)

    elif val.value in "*":
        parent = val
        left = operandos.pop()

        nodo = Node(parent = parent, left = left, direct=direct)
        operandos.push(nodo)

res = operandos.pop()

if direct:

    print("\n\nMétodo directo")
    cadena = input("Ingrese la cadena a simular: ") or "bab"

    # Agregar símbolo terminal
    concat = Symbol('.')
    hashtagSymbol = Symbol('#', number=number+1)
    hashtag = Node(parent=hashtagSymbol, direct=direct)
    alphabetNumbers[number+1] = hashtagSymbol
    alphabet.append('#')
    hashtagNumber = number

    # Añadir nodo terminal
    tree = Node(parent=concat, left=res, right=hashtag, direct=direct)
    treeTuple = tree.printNode()

    # Visualización de árbol
    graph = Digraph()
    tree.add_nodes(graph, treeTuple)
    graph.render('./treeImage/tree', format='png', view=True)

    # ----------------------------- Construcción directa -----------------------------
    # Paso 1: Construcción de tabla siguiente posición
    # # Seleccionar cada uno de los nodos concat y kleene para construir tabla

    pending = Stack() # Para almacenar los nodos por analizar
    pending.push(tree) # Paso base
    siguientePosicion = {}

    while not pending.isEmpty():

        nodeTemp = pending.pop()

        # Siguiente Posición para caso en donde el valor del nodo derecho sea #
        if isinstance(nodeTemp.right, Node) and isinstance(nodeTemp.right.parent, Symbol) and nodeTemp.right.parent.value == '#':
            i = nodeTemp.right.parent.number
            if i not in siguientePosicion.keys():
                    siguientePosicion[i] = {}
                    for c in alphabet:
                        siguientePosicion[i][c] = set()

        # Siguiente Posición de concatenación
        if nodeTemp.parent.value == ".":
            t = nodeTemp.left.ultimaPosicion()
            for i in t:
                getAlphabet = alphabetNumbers[i].value

                # Agregar sets vacíos para cada valor del input
                if i not in siguientePosicion.keys():
                    siguientePosicion[i] = {}
                    for c in alphabet:
                        siguientePosicion[i][c] = set()

                # print(siguientePosicion)
                if i in siguientePosicion.keys() and getAlphabet in siguientePosicion[i].keys():
                    for j in nodeTemp.right.primeraPosicion():
                        siguientePosicion[i][getAlphabet].add(j)

        # Siguiente Posición Cerradura de Kleene
        elif nodeTemp.parent.value == "*":
            t = nodeTemp.ultimaPosicion()
            for i in t:

                # Agregar sets vacíos para cada valor del input
                if i in siguientePosicion.keys():
                    for c in alphabet:
                        if c not in siguientePosicion[i].keys():
                            siguientePosicion[i] = {c: set()}

                getAlphabet = alphabetNumbers[i].value
                for j in nodeTemp.primeraPosicion():
                    siguientePosicion[i][getAlphabet].add(j)

        if nodeTemp.left is not None and nodeTemp.right is not None:
            # Push a stack
            pending.push(nodeTemp.right)
            pending.push(nodeTemp.left)

        elif nodeTemp.left is not None:
            pending.push(nodeTemp.left)

    # Paso 2: Construcción de tabla de transiciones
    transiciones = {}
    D_states = set()

    simboloPrimerEstado = ''
    primerEstado = ''

    for key, value in siguientePosicion[1].items():
        if value != set():
            simboloPrimerEstado = key, 
            primerEstado = value

    states = Stack()
    states.push(primerEstado)

    while not states.isEmpty():
        state = tuple(states.pop())

        # Por cada valor del alfabeto recorrer la siguiente pos de cada estado state (que es un set)
        if state not in D_states:
            D_states.add(state)
            transiciones[state] = {}
            for c in alphabet:
                transiciones[state].update({c: set()})

        state = list(state)
        nextPos = ''
        for n in state:
            for c in alphabet:
                nextPos = siguientePosicion[n][c]
                nextPos = tuple(nextPos)
                transiciones[tuple(state)][c].update(nextPos)

                # Agregar nuevo estado
                if nextPos != "" and nextPos != () and nextPos not in D_states:
                    states.push(nextPos)

   # Estados finales
    finalStates = list(filter(lambda x: hashtagNumber in x, D_states))

    # Crear AFD
    afdDirecto = AFD(
                    Q = D_states,
                    q_start = primerEstado,
                    q_end = finalStates,
                    transitions = transiciones,
                    alphabet = alphabet
                 )
    
    # Imprimir AFD
    afdDirecto.to_graphviz(filename = 'afdDirecto')

    # Simular cadena
    afdDirecto.simulacion(cadena)

    # --------------------------------------------------------------------------------

else:

    print("\n\nConstrucción de AFN y AFN mediante Thompson, subconjuntos y minimización")
    cadena = input("Ingrese la cadena a simular: ") or "bab"

    # Visualización de árbol
    treeTuple = res.printNode()
    graph = Digraph()
    res.add_nodes(graph, treeTuple)
    graph.render('./treeImage/tree', format='png', view=True)

    # Thompson
    thompsonAFN = res.thompsonAutomataAFN
    thompsonAFN.to_graphviz(filename='AFN_thompson')
    thompsonAFN.simulacionAFN(cadena)

    # Subconjuntos
    AFDsubset = thompsonAFN.to_AFD()
    AFDsubset.to_graphviz(filename = 'AFD_subset')


    # AFDMinimizado = Minimizacion(AFDsubset)
    # AFDMinimizado = AFDMinimizado.minimize()
    # AFDMinimizado.to_graphviz(filename = 'AFD_minimizado')
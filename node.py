# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

from turtle import left
from types import NoneType
from AFN import AFN
from ctypes import Union
from symbol import Symbol

labelId = 0
epsilon = 'ε'

def label():
    '''
        Asignación de número de estado.
    '''
    global labelId
    state = labelId
    labelId += 1
    return state

class Node:
    """
        Clase para simular un nodo del árbol y creación de autómatas con distintos métodos.
    """

    def __init__(self, parent=None, right = None, left = None):

        # Nodos del árbol
        self.parent: Symbol = parent
        self.right: Union[Symbol, Node] = right
        self.left: Union[Symbol, Node] = left

        # Autómata finito no determinista
        self.thompsonAutomataAFN: AFN = None
        # Llamar funciones de construcción
        self.constructionMethods()


    def printNode(self):

        right = self.right
        left = self.left
        parent = self.parent

        return (
                    self.parent.value if isinstance(parent, Symbol) else self.parent.printNode(),
                    self.left.value if self.left is not None and isinstance(left, Symbol) else (self.left.printNode() if self.left is not None else None),
                    self.right.value if self.right is not None and isinstance(right, Symbol) else (self.right.printNode() if self.right is not None else None)
                )



    # ------------------------ Creación de AFN utilizando thompson ------------------------

    def symbolThompson(self):

        """
            Creación de autómata de symbols.

            (Referencia para construcción: https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Thompson-a-symbol.svg/556px-Thompson-a-symbol.svg.png)
        """
        q_start = label()
        q_end = label()

        self.thompsonAutomataAFN = AFN(
                                Q = [q_start, q_end],
                                q_start = q_start,
                                q_end = q_end,
                                transitions = {q_start: {self.parent.value: [q_end]}},
                                alphabet = [self.parent.value],
                            )

        # self.thompsonAutomataAFN.to_graphviz(filename = 'symbolAFN')
    

    def kleeneThompson(self):

        """
            Creación de AFN mediante Thompson.
            
            (Referencia para construcción: https://i.stack.imgur.com/XTHXI.jpg)
        """

        # Obtener información del nodo left
        leftNode = self.left.thompsonAutomataAFN
        transitions = leftNode.transitions
        alphabet = leftNode.alphabet
        Q = leftNode.Q

        # Nuevo lenguaje
        alphabet.append(epsilon) if epsilon not in alphabet else alphabet

        # Nuevos estados
        q_start = label()
        q_end = label()
        q_states = [q_start, q_end]

        # Nuevas transiciones
        transitions[q_start] = { epsilon: [leftNode.q_start, q_end] }
        transitions[leftNode.q_end] = { epsilon: [leftNode.q_start, q_end]}

        # Nuevos estados
        Q.extend(q_state for q_state in q_states if q_state not in Q)

        self.thompsonAutomataAFN = AFN(
                                Q = Q,
                                q_start = q_start,
                                q_end = q_end,
                                transitions = transitions,
                                alphabet = alphabet
                            )

        # self.thompsonAutomataAFN.to_graphviz(filename = 'kleeneAFN')


    def orThompson(self):

        """
            Creación de AFN mediante Thompson.
            
            (Referencia para construcción: https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Thompson-or.svg/453px-Thompson-or.svg.png)
        """
        # Obtener información de nodos
        # left
        leftNode = self.left.thompsonAutomataAFN
        leftTransitions = leftNode.transitions
        alphabet = leftNode.alphabet
        Q = leftNode.Q

        # right
        rightNode = self.right.thompsonAutomataAFN
        rightTransitions = rightNode.transitions
        alphabet.extend(sym for sym in rightNode.alphabet if sym not in alphabet)
        Q.extend(q_state for q_state in rightNode.Q if q_state not in Q)

        # Unir transiciones
        transitions = {}
        transitions.update(leftTransitions)
        transitions.update(rightTransitions)

        # Nuevas transiciones
        q_start = label()
        q_end = label()
        q_states = [q_start, q_end]
        transitions[q_start] = { epsilon: [leftNode.q_start, rightNode.q_start] }
        transitions[leftNode.q_end] = { epsilon: [q_end] }
        transitions[rightNode.q_end] = { epsilon: [q_end] }

        # Nuevo lenguaje
        alphabet.append(epsilon) if epsilon not in alphabet else alphabet

        # Nuevos estados
        Q.extend(q_state for q_state in q_states if q_state not in Q)

        self.thompsonAutomataAFN = AFN(
                                Q = Q,
                                q_start = q_start,
                                q_end = q_end,
                                transitions = transitions,
                                alphabet = alphabet
                            )

        # self.thompsonAutomataAFN.to_graphviz(filename = 'orAFN')


    def andThompson(self):

        """
            Creación de AFN mediante Thompson.
            
            (Referencia para construcción: https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Thompson-concat.svg/796px-Thompson-concat.svg.png)
        """
        # Obtener información de nodos
        # left
        leftNode = self.left.thompsonAutomataAFN
        leftTransitions = leftNode.transitions
        alphabet = leftNode.alphabet
        Q = leftNode.Q

        # right
        rightNode = self.right.thompsonAutomataAFN
        rightTransitions = rightNode.transitions
        alphabet.extend(sym for sym in rightNode.alphabet if sym not in alphabet) 
        Q.extend(q_state for q_state in rightNode.Q if q_state not in Q)

        # Unir transiciones
        transitions = {}
        transitions.update(leftTransitions)
        transitions.update(rightTransitions)
        transitions[leftNode.q_end] = { epsilon: [rightNode.q_start]}

        # Update de start y end node
        q_start = leftNode.q_start
        q_end = rightNode.q_end

        self.thompsonAutomataAFN = AFN(
                                Q = Q,
                                q_start = q_start,
                                q_end = q_end,
                                transitions = transitions,
                                alphabet = alphabet
                            )

        # self.thompsonAutomataAFN.to_graphviz(filename = 'andAFN')


# -------------------------------------------------------------------------------------


# --------------------- Creación de AFN utilizando método directo ---------------------

    def 

# -------------------------------------------------------------------------------------

    def constructionMethods(self):

        if self.parent.notOperator():
            self.symbolThompson()
        elif self.parent.value == '*':
            self.kleeneThompson()
        elif self.parent.value == '|':
            self.orThompson()
        elif self.parent.value == '.':
            self.andThompson()
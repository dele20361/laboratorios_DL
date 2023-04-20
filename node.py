# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# from AFN import AFN
# from AFD import AFD
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

    def __init__(self, parent=None, right = None, left = None, direct = False):

        # Nodos del árbol
        self.parent: Symbol = parent
        self.right: Union[Symbol, Node] = right
        self.left: Union[Symbol, Node] = left

        self.tree = None
        # Método para construcción de AFD
        # # direct: False -> Thompson y minimización
        # # direct: True -> Directo y minimización
        self.direct: bool = direct

        # Autómata finito no determinista
        self.thompsonAutomataAFN: AFN = None

        # Llamar funciones de construcción
        if not direct :
            self.constructionMethods()


    def deepcopy_node(self, node):
        new_node = Node(parent=node.parent, right=node.right, left=node.left, direct=node.direct)

        if isinstance(node.left, Node):
            new_node.left = self.deepcopy_node(node.left)
        else:
            new_node.left = node.left

        if isinstance(node.right, Node):
            new_node.right = self.deepcopy_node(node.right)
        else:
            new_node.right = node.right

        return new_node


    def printNode(self):

        right = self.right
        left = self.left
        parent = self.parent

        self.tree = (
                    [parent.value, parent.number] if isinstance(parent, Symbol) and parent.number != None else ( parent.value if isinstance(parent, Symbol) else parent.printNode()),
                    [left.value, "left.number"] if self.left is not None and isinstance(left, Symbol) else ( left.printNode() if left is not None else None),
                    [right.value, "right.number"] if self.right is not None and isinstance(right, Symbol) else ( right.printNode() if right is not None else None)
                    )
        
        return self.tree


    def add_nodes(self, graph, node):
        """
            Visualización de árbol sintáctico.
        """
        if node is None:
            return None
        
        if type(node) == tuple:
            parent = str(id(node))
            graph.node(parent, str(node[0]), shape='circle', style='filled', fillcolor="#D4EFDF", color='#7DCEA0')
            for child in node[1:]:
                child_id = self.add_nodes(graph, child)
                if child_id:
                    graph.edge(parent, str(child_id), color='#7DCEA0')
            return parent
        else:
            node_id = str(id(node))
            graph.node(node_id, str(node))
            return node_id


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


    def constructionMethods(self):

        if self.parent.notOperator():
            self.symbolThompson()
        elif self.parent.value == '*':
            self.kleeneThompson()
        elif self.parent.value == '|':
            self.orThompson()
        elif self.parent.value == '.':
            self.andThompson()

# -------------------------------------------------------------------------------------


# --------------------- Creación de AFN utilizando método directo ---------------------

    def anulable(self):

        match self.parent.value:
            case 'ε':
                return True
            case '*':
                return True
            case '|':
                return self.left.anulable() or self.right.anulable()
            case '.':
                return self.left.anulable() and self.right.anulable()

        if self.parent.number:
            return False


    def primeraPosicion(self):

        match self.parent.value:
            case 'ε':
                return {}
            case '*':
                return self.left.primeraPosicion()
            case '|':
                return self.left.primeraPosicion().union(self.right.primeraPosicion())
            case '.':
                if self.left.anulable():
                    return self.left.primeraPosicion().union(self.right.primeraPosicion())
                else:
                    return self.left.primeraPosicion()
        
        if self.parent.number is not None:
            return {self.parent.number}


    def ultimaPosicion(self):

        match self.parent.value:
            case 'ε':
                return {}
            case '*':
                return self.left.ultimaPosicion()
            case '|':
                return self.left.ultimaPosicion().union(self.right.ultimaPosicion())
            case '.':
                if self.right.anulable():
                    return self.left.ultimaPosicion().union(self.right.ultimaPosicion())
                else:
                    return self.right.ultimaPosicion()
        
        if self.parent.number is not None:
            return {self.parent.number}

# -------------------------------------------------------------------------------------
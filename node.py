# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

from AFD import AFD
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

    def __init__(self, parent=None, right = None, left = None, direct = True, followpos = {}):

        # Nodos del árbol
        self.parent: Symbol = parent
        self.right: Union[Symbol, Node] = right
        self.left: Union[Symbol, Node] = left

        self.tree = None
        self.direct: bool = direct

        self.followpos = followpos
        self.primeraPosicion()
        self.ultimaPosicion()
        self.siguientePosicion(self.followpos)


    def deepcopy_node(self, number):

        if self.left is None and self.right is None:
            return Node(parent=Symbol(self.parent.value, number=number)), number + 1

        new_node = Node(parent=self.parent, right=self.right, left=self.left, direct=self.direct)

        if isinstance(self.left, Node):
            new_node.left, number = self.left.deepcopy_node(number)
        if isinstance(self.right, Node):
            new_node.right, number = self.right.deepcopy_node(number)

        return new_node, number


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


# --------------------- Creación de AFN utilizando método directo ---------------------

    def anulable(self):

        if self.parent.value == 'ε' and not self.parent.notOp:
            return True

        elif  self.parent.value == '*' and not self.parent.notOp:
            return True

        elif  self.parent.value == '|' and not self.parent.notOp:
            return self.left.anulable() or self.right.anulable()

        elif  self.parent.value == '+' and not self.parent.notOp:
            return self.left.anulable()

        elif  self.parent.value == '.' and not self.parent.notOp:
            return self.left.anulable() and self.right.anulable()


        if self.parent.number:
            return False


    def primeraPosicion(self):

        if self.parent.value == 'ε' and not self.parent.notOp:
            return {}
        elif self.parent.value ==  '*' and not self.parent.notOp:
            return self.left.primeraPosicion()

        elif self.parent.value ==  '+' and not self.parent.notOp:
            return self.left.primeraPosicion()

        elif self.parent.value ==  '|' and not self.parent.notOp:
            return self.left.primeraPosicion().union(self.right.primeraPosicion())

        elif self.parent.value ==  '.' and not self.parent.notOp:
            if self.left.anulable():
                return self.left.primeraPosicion().union(self.right.primeraPosicion())
            else:
                return self.left.primeraPosicion()
        
        if self.parent.number is not None:
            return {self.parent.number}


    def ultimaPosicion(self):

        if self.parent.value == 'ε':
            return {}

        elif self.parent.value == '*' and not self.parent.notOp:
            return self.left.ultimaPosicion()
        
        elif self.parent.value == '+' and not self.parent.notOp:
            return self.left.ultimaPosicion()

        elif self.parent.value == '|' and not self.parent.notOp:
            return self.left.ultimaPosicion().union(self.right.ultimaPosicion())

        elif self.parent.value == '.' and not self.parent.notOp:
            if self.right.anulable():
                return self.left.ultimaPosicion().union(self.right.ultimaPosicion())
            else:
                return self.right.ultimaPosicion()
        
        if self.parent.number is not None:
            return {self.parent.number}


    def siguientePosicion(self, followpos:list=None):

        if self.parent.value == '*' and not self.parent.notOp:
            for i in self.ultimaPosicion():
                if i in self.followpos:
                    self.followpos[i] = self.followpos[i].union(self.primeraPosicion())
                else:
                    self.followpos[i] = self.primeraPosicion()

        elif self.parent.value == '+' and not self.parent.notOp:
            for i in self.ultimaPosicion():
                if i in self.followpos:
                    self.followpos[i] = self.followpos[i].union(self.primeraPosicion())
                else:
                    self.followpos[i] = self.primeraPosicion()

        elif self.parent.value == '.' and not self.parent.notOp:
            for i in self.left.ultimaPosicion():
                if i in self.followpos:
                    self.followpos[i] = self.followpos[i].union(self.right.primeraPosicion())
                else:
                    self.followpos[i] = self.right.primeraPosicion()
            pass


# -------------------------------------------------------------------------------------
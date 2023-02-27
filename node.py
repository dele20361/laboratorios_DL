# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para simular un nodo

from multiprocessing.sharedctypes import Value


class Node:

    def __init__(self, parent=None, right = None, left = None):
        # self.value = value
        self.right = right
        self.left = left
        self.parent = parent

    def printNode(self):
        print(""""

            - parent: {}
            - left: {}
            - right: {}
        """.format(self.parent.value, self.left, self.right.value))
    
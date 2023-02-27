from tracemalloc import start
from unicodedata import name


class State:

    def __init__(self, name):
        self.name = name
        self.transitions = []

    def addTransition(self, inputVal, to):
        """
            Función para agregar una transición.
            Esquema de transición: [estado actual, input, estado al que llegará]
            
            Parámetros:
            -----------
            - inputVal: input para indicar la transición (symbol obj)
            - to: estado al que se moverá dado el input (state obj)
        """ 
        self.transitions.append([self, inputVal, to])


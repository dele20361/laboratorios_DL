# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio B

from gettext import translation
from graphviz import Digraph
from Automata import Automata


class AFD(Automata):

    def __str__(self) -> str:
        return super().__str__()

    def generate_nodes(self, g):
        # Agregar los nodos
        for q in self.Q:
            if q == self.q_start:
                node_color = '#FCF3CF'
                g.node(str(q), shape='circle', style='filled', fillcolor=node_color, color='black')
            elif q in self.q_end:
                node_color = '#7DCEA0'
                g.node(str(q), shape='doublecircle', style='filled', fillcolor=node_color, color='black') 
            else: 
                node_color = '#FFFFFF'
                if str(q) != "()":
                    g.node(str(q), shape='circle', style='filled', fillcolor=node_color, color='black')

    def generate_edges(self, g):
        # Agregar las transiciones
        for i in self.Q:
            startNode = i
            transitions = self.transitions[i]
            for j in transitions:
                if len(transitions[j]) > 0:
                    symbol = j
                    endNode = transitions[j]
                    g.edge(str(tuple(startNode)), str(tuple(endNode)), label=symbol)
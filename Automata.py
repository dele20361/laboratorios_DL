# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio B

from graphviz import Digraph

class Automata():
    """
        Clase padre de AFN y AFD.
    """

    def __init__(self, Q, q_start, q_end, transitions, alphabet):
        self.Q = Q
        self.q_start = q_start
        self.q_end = q_end
        self.transitions = transitions
        self.alphabet = alphabet

    def generate_nodes(self, g):
        # Agregar los nodos
        for q in self.Q:
            if q == self.q_start:
                node_color = '#FCF3CF'
                g.node(str(q), shape='circle', style='filled', fillcolor=node_color, color='black')
            elif q == self.q_end:
                node_color = '#7DCEA0'
                g.node(str(q), shape='doublecircle', style='filled', fillcolor=node_color, color='black') 
            else: 
                node_color = '#FFFFFF'
                if str(q) != "()":
                    g.node(str(q), shape='circle', style='filled', fillcolor=node_color, color='black')

    def generate_edges(self,g):
        # Agregar las transiciones
        for q, t in self.transitions.items():
            for symbol, next_states in t.items():
                for next_state in next_states:
                    g.edge(str(q), str(next_state), label=symbol)

    def to_graphviz(self, filename = 'afn'):
        """
            Generación de imagen para visualización de autómata
        """
        g = Digraph('AFN', graph_attr={'rankdir': 'LR'})

        g.attr('node', shape='circle', fontname='Helvetica', fontsize = '14', penwidth='0.75')
        g.attr('edge', fontname='Helvetica', fontsize = '14', penwidth='0.75')

        self.generate_nodes(g)
        self.generate_edges(g)

        filename = './automataImage/' + filename
        format = 'jpg'
        view = True

        try:
            g.render(filename, format=format, view=view, cleanup=True)
            print(f"Autómata generado en {filename}.{format}")
        except Exception as e:
            print(f"Error al generar imagen del autómata: {e}")

        return g

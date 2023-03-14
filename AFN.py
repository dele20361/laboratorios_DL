# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para la construcción de AFN


from graphviz import Digraph

class AFN:
    def __init__(self, Q, q_start, q_end, transitions, alphabet):
        self.Q = Q
        self.q_start = q_start
        self.q_end = q_end
        self.transitions = transitions
        self.alphabet = alphabet

    def to_graphviz(self, filename = 'afn'):
        g = Digraph('AFN')

        # Agregar los nodos
        for q in self.Q:
            if q == self.q_start:
                g.node(str(q), shape='circle', color='#7DCEA0', style='filled')  # Hacer que q_start sea verde
            elif q == self.q_end:
                g.node(str(q), shape='doublecircle', color='#DC451C', style='filled')
            else:
                g.node(str(q), shape='circle')

        # Agregar las transiciones
        for q, t in self.transitions.items():
            for symbol, next_states in t.items():
                for next_state in next_states:
                    g.edge(str(q), str(next_state), label=symbol)

        filename = './automataImage/' + filename
        format = 'jpg'
        view = True

        try:
            g.render(filename, format=format, view=view, cleanup=True)
            print(f"Autómata generado en {filename}.{format}")
        except Exception as e:
            print(f"An error occurred while rendering the AFN: {e}")

        return g

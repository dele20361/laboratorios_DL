from stack import Stack
from graphviz import Digraph

class LR0():

    def __init__(self, productions, tokens) -> None:
        self.productions = productions
        self.productionRules = productions
        self.tokens = tokens
        self.q_init = []
        self.q_end = ['accept']
        self.transitions = []
        self.states = []
        self.generateAutomata()
        self.first = {}
        self.follow = {}
        self.firstF()
        self.followF()

    def move(self, symbol: str, items: list, stack: Stack) -> list:
        next_state = []
        closureNext = []
        for item in items:
            if isinstance(item, list):
                item = item[0]
            # Busco dónde está el puntito
            prod = item[1]
            dot_pos = prod.index('.')
            # Miro si lo que está a la derecha del punto es el símbolo.
            if len(prod) > dot_pos + 1 and prod[dot_pos + 1] == symbol:
                # Mover el punto
                copy = list(item[1])
                punto = copy.pop(dot_pos)
                copy.insert(dot_pos + 1, punto)
                next_state.append((item[0], copy))

        if next_state:
            # Almacenar transición
            for i in next_state:
                destine = self.Closure(i, items)
                for j in destine:
                    closureNext.append(j)
            
            # Hacer estructura de transición
            nextS = (items, symbol, closureNext)

            # Añadir transición
            if nextS not in self.transitions:
                self.transitions.append(nextS)

            # Push a stack
            if nextS[2] not in self.states:
                self.states.append(nextS[2])
                stack.push(nextS[2])


    def Closure(self, evaluatingProd, items) -> list:
        state = [evaluatingProd]
        stateStack = Stack()
        stateStack.push(evaluatingProd)
        rightEvaluated = set()

        while not stateStack.isEmpty():
            evaluatingProd = stateStack.pop()

            # Buscar pos del puntito
            if len(evaluatingProd) > 1:
                prod = list(evaluatingProd[1])
                puntitoPos = prod.index('.')
                if len(prod) > puntitoPos + 1:
                    # Obtener lo que está al lado derecho del puntito
                    right = prod[puntitoPos + 1]
                    # Verificar si es un no terminal
                    if right.islower() and right not in rightEvaluated:
                        rightEvaluated.add(right)
                        for izq, der in self.productionRules:
                            # Buscar transiciones que tengan en el lado 
                            # derecho el estado no terminal right
                            if izq == right:
                                new_prod = (izq, der)
                                state.append(new_prod)
                                stateStack.push(new_prod)

        return state



    def generateAutomata(self):

        items = []
        statesStack = Stack()

        # Agregar producción aumentada
        firstElement = next(iter(self.productionRules))[0]
        tempFirst = firstElement + "'"
        temp = (tempFirst, [firstElement])
        self.productionRules.insert(0, temp)
        self.q_init = temp

        # Crear items
        for clave, value in self.productionRules:
            value.insert(0, '.')
            items.append((clave, value))

        statesStack.push(items)
        self.states.append(items)

        while not statesStack.isEmpty():

            # Ahora items es esto
            items = statesStack.pop()

            # Ver donde está el puntito
            for produccion in items:
                if isinstance(produccion,list):
                    produccion = produccion[0]

                prod = produccion[1]
                puntitoPos = prod.index('.')
                if len(prod) > puntitoPos + 1:
                    # Lo que está a la derecha es terminal? (Mayúsculas)
                    right = prod[puntitoPos + 1]
                    if right.islower():
                        state = produccion
                        break

            if state:
                # Con ese state calcular move
                for terminal in self.tokens:
                    self.move(terminal, items, statesStack)

                for nonTerminal in self.productionRules:
                    newState = self.move(nonTerminal[0], items, statesStack)

        # Buscar transición que tiene self.q_init
        final_transition = []
        for i in self.states:
            if any(tempFirst in t for t in i):
                final_transition = i

        # Añadir transición final
        self.states.append(self.q_end)
        self.transitions.append((final_transition, '$', self.q_end))
        # self.to_graphviz()


    def firstF(self):
        first = {}
        
        # Inicializar el conjunto FIRST para cada símbolo no terminal
        for non_terminal, _ in self.productionRules:
            first[non_terminal] = set()
        
        while True:
            updated = False
            
            for non_terminal, right in self.productionRules:
                first_element = right[1]  # El primer elemento después del punto
                
                if first_element in self.tokens:
                    if first_element not in first[non_terminal]:
                        first[non_terminal].add(first_element)
                        updated = True
                elif first_element != non_terminal:
                    if first_element in first.keys():
                        for elem in first[first_element]:
                            if elem not in first[non_terminal]:
                                first[non_terminal].add(elem)
                                updated = True
            
            if not updated:
                break
        
        self.first = first


    def followF(self):
        # Lista de símbolos no terminales y terminales
        non_terminals = set([prod[0] for prod in self.productionRules])
        terminals = set(self.tokens)

        follow = {symbol: set() for symbol in non_terminals}

        # Caso base símbolo inicial
        startSymbol = self.q_init[0]
        follow[startSymbol[:-1]].add('$')

        while True:
            updated = False

            for left, right in self.productionRules:
                for i in range(len(right)):
                    current_symbol = right[i]

                    if current_symbol in non_terminals:
                        if i == len(right) - 1:
                            prev_follow_size = len(follow[current_symbol])
                            follow[current_symbol].update(follow[left])
                            if len(follow[current_symbol]) != prev_follow_size:
                                updated = True
                        else:
                            next_symbol = right[i + 1]
                            if next_symbol in terminals:
                                prev_follow_size = len(follow[current_symbol])
                                follow[current_symbol].add(next_symbol)
                                if len(follow[current_symbol]) != prev_follow_size:
                                    updated = True
                            elif next_symbol in non_terminals:
                                prev_follow_size = len(follow[current_symbol])
                                next_symbols = self.first[next_symbol]
                                follow[current_symbol].update(next_symbols)
                                follow[current_symbol].discard('')
                                if len(follow[current_symbol]) != prev_follow_size:
                                    updated = True

            if not updated:
                break

        self.follow = follow


    # --------------------------------------------- GRAFICAR --------------------------------------------- #

    def generate_nodes(self, g):
        # Agregar los nodos
        for q in self.states:
            if self.q_init in q:
                node_color = '#FCF3CF'
                g.node(str(q), shape='box', style='filled', fillcolor=node_color, color='black')
            elif self.q_end == q:
                node_color = '#7DCEA0'
                g.node(str(q), shape='box', style='filled', fillcolor=node_color, color='black') 
            else: 
                node_color = '#FFFFFF'
                if str(q) != "()":
                    g.node(str(q), shape='box', style='filled', fillcolor=node_color, color='black')


    def generate_edges(self,g):
        # Agregar las transiciones
        for transicion in self.transitions:
            # print(transicion[0])
            g.edge(str(transicion[0]), str(transicion[2]), label=transicion[1])


    def to_graphviz(self, filename = 'lr4'):
        """
            Generación de imagen para visualización de autómata
        """
        g = Digraph('LR', graph_attr={'rankdir': 'LR'})

        g.attr('node', shape='square', fontname='Helvetica', fontsize = '14', penwidth='0.75')
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



if __name__ == '__main__':

    # ------------------ Para mostrar árbol de tokens individuales ------------------ #
    lr0 = LR0([('expression', ['expression', 'PLUS', 'term']), ('expression', ['term']), ('term', ['term', 'TIMES', 'factor']), ('term', ['factor']), ('factor', ['LPAREN', 'expression', 'RPAREN']), ('factor', ['ID'])], ['ID', 'PLUS', 'TIMES', 'LPAREN', 'RPAREN'])
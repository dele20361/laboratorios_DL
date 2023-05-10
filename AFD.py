# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio B

from Automata import Automata


class AFD(Automata):

    def __init__(self, Q, q_start, q_end, transitions, alphabet, hashtagNumbers, hashtagToken):
        self.hashtagNumbers = hashtagNumbers
        self.hashtagToken = hashtagToken
        super().__init__(Q, q_start, q_end, transitions, alphabet)


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


    def simulacion(self, cadena):
        """
            Simulación de una cadena en autómata.
        """
        listCadena = list(cadena)
        state = self.q_start
        recognizedTokens = {}
        token = []

        while listCadena:

            c = listCadena.pop(0)

            if c == '\\':
                nextC = listCadena.pop(0)
                c = c + nextC

            # Calcular estados alcanzables con valor del input
            if c in self.transitions[tuple(state)].keys():
                state = tuple(self.transitions[tuple(state)][c])

                added = False
                for i in self.hashtagNumbers:
                    if i in state and i in self.hashtagToken and not added:
                        if len(token) > 0 and self.hashtagToken[i] != token[-1]:
                            token.append(self.hashtagToken[i])
                            added = True
                        elif len(token) == 0 and self.hashtagToken[i] not in token:
                            token.append(self.hashtagToken[i])
                            added = True
                        
            else:
                error = '@! Error léxico. No se encontró una transición para el caracter "' + c + '"'
                token.append(error)

        if state in self.q_end:
            if not any("@!" in elem for elem in token):
                recognizedTokens[cadena] = list(token)[-1]
            else:
                recognizedTokens[cadena] = list(token)
                return recognizedTokens
        else:
            if len(token) != 0:
                return False
            else:
                return recognizedTokens

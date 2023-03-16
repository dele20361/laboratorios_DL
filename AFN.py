# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para la construcción de AFN

from numpy import sort
from AFD import AFD
from Automata import Automata
from stack import Stack, toStack

epsilon = 'ε'

class AFN(Automata):

    def __init__(self, Q, q_start, q_end, transitions, alphabet):
        super().__init__(Q, q_start, q_end, transitions, alphabet)

    def closure(self):
        """
            Dado un estado, calcular su cerradura epsilon.

            Parámetros:
            - 
        """

        states = Stack()
        transitions = self.transitions
        [states.push(i) for i in transitions.keys()]
        closure = []

        while not states.isEmpty():
            state = states.pop()
            if state not in closure:
                # Obtener transiciones epsilon de estado
                recheable = []
                if epsilon in transitions[state]:
                    for i in transitions[state][epsilon]:
                        recheable.append(i)

                
                closure.append({state: recheable})

        return closure

    def to_AFD(self):

        stack = Stack()
        newTransitions = {}
        D_states = [] # Estados alcanzables. Subconjuntos
        acceptance_states = set() # Estados de aceptación/finales
        epsilon_closure = self.closure() # Cálculo de cerradura epsilon.
        newAlphabet = [symbol for symbol in self.alphabet if symbol != epsilon]

        # Paso base: Agregar estado inicial
        stack.push([self.q_start])

        while not stack.isEmpty():
            state = stack.pop()

            # Calcular nuevos estados
            newState = set()
            [newState.add(i) for i in state]
            for i in epsilon_closure:
                for j in state:
                    if j in i.keys():
                        [newState.add(estado) for estado in i[j]]

            # Definir transiciones
            transitions_alphabet = {}
            for c in newAlphabet:
                destine = []
                for q in newState:
                    # Obtener estados alcanzables
                    if q != self.q_end and c in self.transitions[q].keys():
                        temp = [i for i in self.transitions[q][c] if i not in newState]
                        destine.extend(temp) 
                    if q != self.q_end and epsilon in self.transitions[q].keys() :
                        temp = [i for i in self.transitions[q][epsilon] if i not in newState]
                        destine.extend(temp) 
                    
                # Ver si los estados destino tienen transiciones epsilon por agregar
                for i in destine:
                    temp = []
                    for j in epsilon_closure:
                        if i in j.keys():
                            [temp.append(estado) for estado in j[i] if estado not in temp]
                    destine.extend(temp)            

                transitions_alphabet[c] = destine

            # Agregar nuevos estados a D_states y stack
            for q_states in (transitions_alphabet.values()):
                if len(q_states) > 0:
                    stack.push(q_states)

            # Agregar transitions de iteración a transitions generales
            newTransitions[tuple(newState)] = transitions_alphabet
        
        # Definir estados alcanzables
        D_states = newTransitions.keys()

        # Definir estados de aceptación/finales
        for q in D_states:
            if self.q_end in q:
                acceptance_states.add(q)
        
        # Definir estados de aceptación/finales
        start = (list(D_states)[0])

        return AFD(
            Q = D_states,
            q_start = start,
            q_end = acceptance_states,
            transitions = newTransitions,
            alphabet = newAlphabet
        )
            
# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para la construcción de AFN

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
                        if i not in recheable:
                            recheable.append(i)

                closure.append({state: recheable})

        return closure


    def state_closure(self, state, epsilon_closure, setRes):
        for close in epsilon_closure:
            if state in close.keys():
                for estado in close[state]:
                    setRes.add(estado)
                    self.state_closure(estado, epsilon_closure, setRes)
        
        return setRes


    def to_AFD(self):

        stack = Stack()
        newTransitions = {}
        D_states = set() # Estados alcanzables. Subconjuntos
        acceptance_states = set() # Estados de aceptación/finales
        epsilon_closure = self.closure() # Cálculo de cerradura epsilon.
        newAlphabet = [symbol for symbol in self.alphabet if symbol != epsilon]

        # Paso base: Agregar cerradura epsilon del estado inicial
        setRes = set()
        self.state_closure(self.q_start, epsilon_closure, setRes)
        stack.push(setRes)

        while not stack.isEmpty():
            newState = stack.pop()

            # Definir transiciones
            transitions_alphabet = {}
            for c in newAlphabet:
                destine = set()

                # Ver a qué estados puedo llegar con input c desde el estado newState
                for q in newState:
                    # Obtener estados alcanzables
                    if q != self.q_end and q in self.transitions.keys() and c in self.transitions[q].keys():
                        [destine.add(i) for i in self.transitions[q][c]] 
                    
                # Ver si los estados destino tienen transiciones epsilon por agregar
                newTran = set()
                for s in destine:
                    resSet = set()
                    temp = self.state_closure(s, epsilon_closure, resSet)
                    [newTran.add(i) for i in temp]
                [destine.add(i) for i in newTran]

                # Agregar transición 
                transitions_alphabet[c] = (destine)

                # Push al stack de estado al que llegó
                if destine:
                    if tuple(destine) not in D_states and destine != set():
                        D_states.add(tuple(destine))
                        stack.push(list(destine))

                    if self.q_end in destine:
                        acceptance_states.add(tuple(destine))
            
            # Agregar transitions de iteración a transitions generales
            newTransitions[tuple(newState)] = transitions_alphabet
        
        # Definir estados alcanzables
        D_states = newTransitions.keys()

        # Crear AFD
        return AFD(
            Q = D_states,
            q_start = tuple(setRes),
            q_end = acceptance_states,
            transitions = newTransitions,
            alphabet = newAlphabet
        )
            
    def simulacion(self, cadena):
        """
            Simulación de una cadena en autómata.
        """
        cadena = list(cadena)
        state = self.q_start
        prevState = None

        while len(cadena) > 0:

            c = cadena.pop(0)

            # Calcular cerradura de epsilon
            res = set()
            cerradura_epsilon = self.closure()
            cerraduraEstado = self.state_closure(state, cerradura_epsilon, res)

            # Calcular estados alcanzables con valor del input
            for i in cerraduraEstado:
                if i != self.q_end and c in self.transitions[i].keys():
                    state = tuple(self.transitions[i][c])[0]
                    break

            if state == prevState:
                print('@! Cadena no aceptada. No se encontró una transición para el caracter "', c, '"')
                return False
                
            # Actualizar el estado anterior
            prevState = state

        # Verificar si llegó a un estado de aceptación
        finalizado = [state]
        cerraduraEstado = self.state_closure(state, cerradura_epsilon, res)
        finalizado.extend(cerraduraEstado)

        if self.q_end in finalizado:
            print(">> La cadena pertenece al lenguaje. ")
            return True
        else:
            print('@! Cadena no aceptada. No se llegó a un estado de aceptación.')
            return False

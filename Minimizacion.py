from AFD import AFD


class Minimizacion():
    def __init__(self, afd) -> None:
        self.afd = afd
        self.minimizar()

    def buscar_valor(self, diccionario, valor):
        for clave, valor_actual in diccionario.items():
            if valor in valor_actual:
                return clave
        raise ValueError(f'El valor {valor} no se encuentra en el diccionario')

    def minimizar(self):
        # Paso base
        # Separar en 2 grupos de estados: de aceptación y el resto de estados
        acceptanceStates = self.afd.q_end
        nonAcceptanceStates = self.afd.Q - acceptanceStates

        hashGroups = {} # Diccionario en donde se almacenarán los conjuntos de estados con su tag
        groups = [] # Lista en donde se almacenarán los conjuntos de estados
        transitions = {} # Tablas de transiciones.
        number = 0 # Número para definir transiciones

        # Agregar paso base a lista de estados
        groups.append(acceptanceStates)
        groups.append(nonAcceptanceStates)

        while len(groups) != 0:
            # Agregar identificador de grupos
            limit = len(groups)
            print(">> groups", groups)
            for i in range(limit):
                value = groups.pop(0)
                number = number + 1 
                hashGroups["G" + str(number)] = value

            # Definir tablas de transición
            tabla = {}
            for key, groupstate in hashGroups.items():
                tabla[key] = {}
                for state in groupstate:
                    tabla[key][state] = {}

            for key, groupstate in hashGroups.items():
                for state in groupstate:
                    # Miro a qué estado llego con el input del alfabeto
                    for ch in self.afd.alphabet:
                        normalDestine = self.afd.transitions[state][ch]
                        if normalDestine != set():
                            destineIn = (self.buscar_valor(hashGroups, tuple(normalDestine)))
                            tabla[key][state][ch] = destineIn

            # Verificar qué estados se pueden generar
            for key, transitionGroup in tabla.items():
                # Diccionario de transiciones de cada conjunto de estados
                transitions = {}
                for states, trans in transitionGroup.items():
                    trans_str = str(trans)  # Convertir a string para poder usar como clave en el diccionario
                    if trans_str in transitions:
                        transitions[trans_str].append(states)
                    else:
                        transitions[trans_str] = [states]

                # Encontrar estados con las mismas transiciones
                iguales = {}
                diferentes = {}
                for states_list in transitions.values():
                    if len(states_list) > 1:
                        # Si hay más de un estado en la lista, significa que tienen las mismas transiciones
                        for states in states_list:
                            iguales[states] = transitionGroup[states]
                    else:
                        # Si sólo hay un estado en la lista, significa que tiene transiciones diferentes
                        state = states_list[0]
                        diferentes[state] = transitionGroup[state]

                # Hacer un merge de los estados iguales
                if len(iguales.values()) > 0:
                    # Unir todas las llaves en una sola tupla
                    new_key_set = set()
                    new_value = list(iguales.values())[0]
                    new_key_set = set(item for key in iguales.keys() for item in key)
                    new_key = tuple(new_key_set)
                    iguales = {new_key: new_value}

                    # Remover estados unidos de groups
                    for group in groups:
                        if set(group).issubset(set(new_key_set)):
                            groups.remove(group)

                    # Agregar nuevos estados a groups
                    groups.extend([new_key])
                    iguales.update(diferentes)

                    # Actualizar hashGroups
                    for k in iguales:
                        h = hash(tuple(sorted(list(iguales[k]))))
                        if h in hashGroups:
                            hashGroups[h].update(iguales[k])
                        else:
                            hashGroups[h] = iguales[k]

        # Creación de AFD minimizado
        # Obtener nuevos estados
        new_Q = set(hashGroups.values())

        # Crear diccionario de transiciones del nuevo AFD
        new_transitions = {}
        for group in new_Q:
            group = tuple(sorted(list(group)))
            new_transitions[group] = {}
            for state in group:
                new_transitions[group][state] = {}
                for ch in self.afd.alphabet:
                    normalDestine = self.afd.transitions[state]
                    normalDestine = normalDestine[ch]
                    if normalDestine != set():
                        destineIn = self.buscar_valor(hashGroups, tuple(normalDestine))
                        new_transitions[group][state][ch] = destineIn

        # Crear nuevos estados de aceptación
        new_q_end = set()
        for group in new_Q:
            for state in group:
                if state in self.afd.q_end:
                    new_q_end.add(group)

        # Crear nuevo estado inicial
        new_q_start = self.buscar_valor(hashGroups, self.afd.q_start)
        new_alphabet = self.afd.alphabet
        new_afd = AFD(new_Q, new_q_start, new_q_end, new_transitions, new_alphabet)

        # Devolver AFD minimizado
        return new_afd


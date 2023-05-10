def generateFile(D_states, primerEstado, finalStates, D_transitions, alphabet, hashtagsNumbers, hashtagToken):
    # Obtener clase
    with open('AFD.py') as archivo:
        codigoAFD = archivo.read()

    with open('Automata.py') as archivo:
        codigoAutomata = archivo.read()

    # Escribe el código fuente en un nuevo archivo
    with open('scanner.py', "w") as archivo:
        archivo.write(codigoAutomata)
        archivo.write(codigoAFD)
        addCode = f"""

# ---------------------------------- MAIN ---------------------------------- #

afdDirecto = AFD(
                Q = {D_states},
                q_start = {tuple(primerEstado)},
                q_end = {finalStates},
                transitions = {D_transitions},
                alphabet = {alphabet},
                hashtagNumbers= {hashtagsNumbers},
                hashtagToken = {hashtagToken}
                )
"""

        nextCode = """
recognizedTokens = {}

# Leer archivo
filepath = 'LabD/tests/text.txt'
with open(filepath, "r") as f:
    lines = f.read()

temp = afdDirecto.simulacion(lines)
recognizedTokens.update(temp) if isinstance(temp, dict) else None      


with open('LabD/recognizedTokens', 'w') as archivo:
    for key, value in recognizedTokens.items():
        archivo.write('----------------------------------------------------------------------------------------------\\n')
        archivo.write('                                            CADENA\\n')
        archivo.write('----------------------------------------------------------------------------------------------\\n')
        archivo.write('{}\\n'.format(key))
        archivo.write('\\n----------------------------------------------------------------------------------------------\\n')
        archivo.write('                                            TOKENS\\n')
        archivo.write('----------------------------------------------------------------------------------------------\\n')
        if isinstance(value, list):
            for v in value:
                archivo.write('{}\\n'.format(v))
        else:
            archivo.write('{}\\n'.format(value))      

"""
        archivo.write(addCode)
        archivo.write(nextCode)
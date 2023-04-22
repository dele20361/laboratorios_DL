def generateFile(D_states, primerEstado, finalStates, D_transitions, alphabet, hashtagsNumbers, hashtagToken):
    # Obtener clase
    with open('AFD.py') as archivo:
        codigoAFD = archivo.read()

    with open('Automata.py') as archivo:
        codigoAutomata = archivo.read()

    # Escribe el código fuente en un nuevo archivo
    with open('parser.py', "w") as archivo:
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
    lines = [line.rstrip() for line in f.readlines()]

for prueba in lines:
    temp = afdDirecto.simulacion(prueba)
    recognizedTokens.update(temp) if isinstance(temp, dict) else None

with open('LabD/recognizedTokens', 'w') as archivo:
    archivo.write('{:<20}{}\\n'.format('Cadena', 'Token'))
    archivo.write('------------------------------------- \\n')
    for key, value in recognizedTokens.items():
        archivo.write('{:<20}{}\\n'.format(key, value))        

"""
        archivo.write(addCode)
        archivo.write(nextCode)
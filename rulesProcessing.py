# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio C

def processRules(code):
    '''
        Procesamiento de reglas para convertir de lista a string.
        Eliminación de comentarios (!to fix).
    '''
    in_comment = False
    output = ''
    i = 0
    while i < len(code):
        if in_comment:
            if code[i:i+2] == '*)':
                in_comment = False
                i += 2
            else:
                i += 1
        else:
            if code[i:i+2] == '(*':
                in_comment = True
                i += 2
            else:
                output += code[i]
                i += 1

    result = output

    return result


def createRulesDictionary(content):
    '''
        Creación de diccionario con reglas de tokens.
    '''
    tokens = {}
    start = 0
    end = 0

    # Obtener líneas
    lines = []
    current_line = ""
    for char in content:
        if char == "\n":
            lines.append(current_line)
            current_line = ""
        else:
            current_line += char
    if current_line != "":
        lines.append(current_line)

    # Definir deccionario de reglas
    # key -> Valor de retorno
    # value -> token
    for line in lines:
        line = line.strip()
        hasReturn = False

        if 'rule' not in line:
            # Obtener index de {} para procesar retornos
            for i, char in enumerate(line):
                if char == '{':
                    start = i + 1
                    hasReturn = True
                elif char == '}':
                    end = i
                    break

            # Añadir reglas a diccionario según estructura
            if hasReturn:
                if 'return ' in line:
                    # Para primer caso, en donde no hay |
                    if (line[0:1]) == '|':
                        value = line[1:start - 1].strip()
                    else:
                        value = line[0:start - 1].strip()

                    # Eliminar comillas de caracteres que no son especiales
                    listValue = list(value)
                    if (value != "'+'" or value != "'.'" or value != "'|'" or value != "'?'" or value != "'*'") and listValue[0] == '"' and listValue[-1] == '"':
                        listValue[0] = ''
                        listValue[-1] = ''
                        strVal = []
                        for i in listValue:
                            strVal += i
                        value = strVal
                    start = line.index("return ") + len("return ")

                key = line[start:end].strip().strip('"')
                tokens[key] = value
            else:
                value = line.strip().replace('"', '')
                if "(*" and "*)" not in value and value != '':
                    key = ""
                    tokens[key] = value

    return tokens

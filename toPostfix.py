# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Módulo del algoritno Shunting para convertir la cadena de infix a postfix

from stack import Stack
from symbol import Symbol
from validations import checkParenthesis

def alphabetF(infix):

    alphabet = set(infix) - set('*+?.|()')
    return list(alphabet)


def infix_to_postfix(infix):

    # Chequear paréntesis
    print("@ Error en paréntesis! Revise la expresión regular.") if not checkParenthesis(infix) else True

    alphabet = alphabetF(infix)
    unitary = ['*', '+', '?'] # Operaciones unarias
    operator_stack = Stack()
    output_queue = []
    last = ''
    i = 0

    # for char in infix:
    while i < len(infix):
        char = infix[i]
        symbol = Symbol(char)

        if char in alphabet or ((i+2) < len(infix) and (char == "'") and infix[i+1] in "+.|*?" and infix[i+2] == "'"):
            
            # Cuando cambio esto se arregla
            if char == '\\':
                symbol = Symbol(str(char + infix[i+1]))
                i = i + 1 

            # Eliminar commillas en valores que sean diferentes a "()+.|*?"
            if (i+2) < len(infix)  and (char == "'" and infix[i+1] not in "+.|*?" and infix[i+2] == "'"):
                symbol = Symbol(infix[i+1])
                i = i + 2
            
            if (last in alphabet) or (last == ")") or (last in unitary):
                # Si el estado previo es unario, ) o pertenece al alfabeto agregar concatenación
                if ( last != ' ') or ((i+2) < len(infix) and (char != "'" and infix[i+2] != "'")):
                    concat = Symbol('.')
                    while (not operator_stack.isEmpty()) and concat.precedence <= operator_stack.peek().precedence:
                        output_queue.append(operator_stack.pop())
                    operator_stack.push(concat)

            output_queue.append(symbol)

            if (i+2) < len(infix)  and (char == "'" and infix[i+1] in "+.|*?" and infix[i+2] == "'"):
                output_queue.extend([Symbol(infix[i+1]), Symbol(infix[i+2])])
                i = i+2


        elif char == '(':
            if (last in alphabet) or last == ")" or last in unitary:
                # Si el estado previo es unario, ) o pertenece al alfabeto agregar concatenación
                concat = Symbol('.')
                while (not operator_stack.isEmpty()) and concat.precedence <= operator_stack.peek().precedence:
                    output_queue.append(operator_stack.pop())
                operator_stack.push(concat)

            operator_stack.push(symbol)

        elif char == ')':
            while ((not operator_stack.isEmpty()) and (operator_stack.peek().value != '(')):
                # Agregar todos los operadores hasta antes de (.
                output_queue.append(operator_stack.pop())
            
            operator_stack.pop()

        else:
            # Operador 
            while not operator_stack.isEmpty() and symbol.precedence <= operator_stack.peek().precedence:
                output_queue.append(operator_stack.pop())
            operator_stack.push(symbol)

        last = char
        i = i + 1

    # Agregar operadores restantes al output
    while not operator_stack.isEmpty():
        output_queue.append(operator_stack.pop())


    # Convertir en str
    postfix = ""
    for symbol in output_queue:
        postfix += symbol.value

    return postfix
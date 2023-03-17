# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Módulo del algoritno Shunting para convertir la cadena de infix a postfix

from stack import Stack
from symbol import Symbol

def alphabetF(infix):

    alphabet = set(infix) - set('*+?.|()')
    return list(alphabet)


def infix_to_postfix(infix):

    alphabet = alphabetF(infix)
    unitary = ['*', '+', '?'] # Operaciones unarias
    operator_stack = Stack()
    output_queue = []
    last = ''

    for char in infix:
        symbol = Symbol(char)

        if char in alphabet:
            if (last in alphabet) or (last == ")") or (last in unitary):
                # Si el estado previo es unario, ) o pertenece al alfabeto agregar concatenación
                concat = Symbol('.')
                while (not operator_stack.isEmpty()) and concat.precedence <= operator_stack.peek().precedence:
                    output_queue.append(operator_stack.pop())
                operator_stack.push(concat)

            output_queue.append(symbol)

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

    # Agregar operadores restantes al output
    while not operator_stack.isEmpty():
        output_queue.append(operator_stack.pop())


    # Convertir en str
    postfix = ""
    for symbol in output_queue:
        postfix += symbol.value

    return postfix
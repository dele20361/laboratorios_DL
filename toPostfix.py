# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Módulo del algoritno Shunting para convertir la cadena de infix a postfix

from stack import Stack, toStack
from symbol import Symbol
from validations import addConcatenations

def notGreater(val, stack):
    try:
        return True if val.precedence <= stack[-1].precedence else False
    except KeyError:
        return False

from collections import deque

def alphabet(regex):
    alphabet = list(regex)

    for op in '+?*.|()':
        if op in alphabet:
            alphabet.remove(op)

    return alphabet

def infix_to_postfix(infix, alphabet):
    output_queue = deque()
    operator_stack = []

    for char in infix:
        symbol = Symbol(char)

        if symbol.notOperator():
            output_queue.append(symbol)

        elif char == '(':
            operator_stack.append(symbol)

        elif char == ')':
            while operator_stack[-1].value != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()

        else:
            while operator_stack and symbol.precedence <= operator_stack[-1].precedence:
                output_queue.append(operator_stack.pop())
            operator_stack.append(symbol)

    while operator_stack:
        output_queue.append(operator_stack.pop())

    postfix = ""
    for symbol in output_queue:
        postfix += symbol.value

    return postfix
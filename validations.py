# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Validaciones de sintáxis

from stack import Stack
from symbol import Symbol

def addConcatenations(stack):
    # Trasladar valores de la regex a un stack
    pos = 0
    newRegex = Stack()

    while stack.size() > 0:
        val = stack.pop()
        newRegex.push(val)

        if stack.size() > 1:
            # Caso en donde hayan dos operandos juntos
            nextVal = stack.last().notOperator()
            if val.notOperator() and nextVal:
                newRegex.push(Symbol("."))

            # Caso en donde haya un Kleene seguido de un operando
            elif val.notOperator() == False and nextVal:
                newRegex.push(Symbol("."))

    # [print(">> ",i.value) for i in ]
    return newRegex

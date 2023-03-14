# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Validaciones de sintáxis

from logging import raiseExceptions
from stack import Stack, toList
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
            nextVal = stack.peek()
            if val and nextVal not in '+?*.|':
                newRegex.push(Symbol("."))

            # Caso en donde haya un Kleene seguido de un operando
            elif val not in '+?*.|' == False and nextVal:
                newRegex.push(Symbol("."))
    
    newRegex = toList(newRegex)
    return newRegex


def notOp(nextVal, regex):
    pass

def kleene(nextVal, regex):
    pass

def positive(nextVal, regex):
    pass

def question(nextVal, regex):
    pass

def andOp(nextVal, regex):
    pass

def orOp(nextVal, regex):
    pass

def parenthesis(nextVal, regex):
    if nextVal.notOperator:
        actual, nextVal = popStack(regex)
        notOp(nextVal, regex)
    else:
        raiseExceptions(' @ Error sintáctico! Se esperaba un valor operando.')

def checker(regex):
    actual, nextVal = popStack(regex)
    if actual.value == '(':
        parenthesis(nextVal, regex)

def popStack(regex):
    actual = regex.pop()
    try:
        nextVal = regex.peek()
    except:
        nextVal = None

    return [actual, nextVal]

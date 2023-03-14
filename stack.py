# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para la estructura de un stack

def toStack(lista):
    stack = Stack()
    [stack.push(i) for i in lista]
    return stack

def toList(stack):
    return [stack.pop() for i in range(stack.size())]

class Stack:
    def __init__(self):
        self.item = []

    def push(self, data):
        self.item.insert(0, data)

    def isEmpty(self):
        return self.item == []

    def pop(self):
        return self.item.pop()

    def peek(self):
        return self.item[-1]

    def last(self):
        return self.item[-1]
    
    def size(self):
        return len(self.item)

    def show(self):
        return (self.item)

    def appendPos(self, pos, value):
        return self.insert(pos, value)
    
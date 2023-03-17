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
        self.top = -1

    def push(self, data):
        self.top += 1
        self.item.append(data)

    def isEmpty(self):
        if self.top == -1:
            return True
        else:
            return False

    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.item.pop()
        else:
            return None

    def peek(self):
        return self.item[-1]

    def show(self):
        return (self.item)
    
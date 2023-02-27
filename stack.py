# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para la estructura de un stack

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
        return self.item[0]
    
    def size(self):
        return len(self.item)

    def show(self):
        return (self.item)

    
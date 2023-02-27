# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para representar cada uno de los caracteres

class Symbol:

    def __init__(self, value):
        self.value = value
        self.ascii = ord(value)
        self.precedence = self.precedence()

    def isNumeric(self):
        return True if self.value.isdigit() else False
    
    def precedence(self):
        match self.value:
            case '(':
                return 4
            case '*':
                return 3
            case '+':
                return 3
            case '?':
                return 3
            case '.':
                return 2
            case '|':
                return 1

        return 0
    
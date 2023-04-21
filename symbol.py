# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Clase para representar cada uno de los caracteres

class Symbol:

    def __init__(self, value, number=None, notOp=None, hashtag=None):
        self.value = str(value)
        self.number = number
        self.hashtag = hashtag if isinstance(hashtag, bool) else False # Bandera para símbolos +*|?. especiales
        # self.ascii = ord(value)
        self.precedence = self.precedence()
        self.notOp = notOp if isinstance(notOp, bool) else False # Bandera para símbolos +*|?. especiales

    def changeNumber(self, number):
        self.number = number
        return self.number

    def notOperator(self):
        return True if self.value not in "()+*|?." or self.notOp == True else False
    
    def precedence(self):
        match self.value:
            case '(':
                return 0
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

    
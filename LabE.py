from math import prod
from stack import toStack

class ProcessYalp:

    def __init__(self, filepath) -> None:
        self.content = self.openFile(filepath)
        self.producciones = ''
        self.tokens = []
        self.createDictionary()


    def openFile(self, filepath="./testsLabE/slr-1.yalp"):
        """ 
            Abrir archivo.
            Parámetos:
            - filename: Path relativo del archivo .yal
        
        """
        with open(filepath, "r") as f:
            content = f.read()

        content = toStack(content)

        return content

    def createDictionary(self):
        c = self.content.pop()

        inComment = False
        productions = ''
        tokens = []

        while not self.content.isEmpty():
            if c == '/' and self.content.peek() == '*':
                inComment = True
                self.content.pop()  
                c = self.content.pop() 

                # Iterar hasta encontrar el final del comentario '*/'
                while c != '*' or self.content.peek() != '/':
                    c = self.content.pop()

                self.content.pop()  
                c = self.content.pop()  
                inComment = False

            elif not inComment:
                if c == '%' and self.content.peek() == 't':
                    for _ in 'token ':
                        self.content.pop()

                    token = ''
                    while c != '\n' and not self.content.isEmpty():
                        c = self.content.pop()
                        if c != '\n' and c != ' ':
                            token += c
                        elif c == ' ':
                            tokens.append(token)
                            token = ''
                            c = self.content.pop()
                            while c != '\n' and not c.isspace() and not self.content.isEmpty():
                                token += c
                                c = self.content.pop()

                    if token:
                        tokens.append(token)

                else:
                    productions += c

            c = self.content.pop()

        # print(tokens)
        productions = toStack(productions)
        self.processProductions(productions)
        self.tokens = tokens

    
    def processProductions(self, productions):
        right = ''
        left = ''
        productionRules = {}

        while not productions.isEmpty():
            c = productions.pop()

            while c != ':' and not productions.isEmpty():
                if c != '\n':
                    left += c
                c = productions.pop()

            while c != ';' and not productions.isEmpty():
                if c != '\n' and c != ':' and c is not None:
                    right += c
                c = productions.pop()

            if left and right:
                productionRules[left] = right.strip()
                left = ''
                right = ''

        # Dividir producciones

        new_productions = {}
        for key, value in productionRules.items():
            start = 0
            for i, char in enumerate(value):
                if char == '|':
                    new_productions.setdefault(key, []).append(value[start:i].strip())
                    start = i + 1
            new_productions.setdefault(key, []).append(value[start:].strip())

        self.producciones = new_productions

        # Separar palabras
        def custom_split(value):
            words = []
            start = 0
            for i in range(len(value)):
                if value[i] == " ":
                    words.append(value[start:i])
                    start = i + 1
            words.append(value[start:])
            return words

        for key, value in self.producciones.items():
            if isinstance(value, list):
                tempValue = []
                for i in value:
                    tempValue.append(custom_split(i))
                self.producciones[key] = tempValue
            else:
                self.producciones[key] = custom_split(value)

        # Convertir a tuplas
        self.producciones = [(clave, valor) for clave, lista in self.producciones.items() for valor in lista]

if __name__ == '__main__':

    # ------------------ Para mostrar árbol de tokens individuales ------------------ #
    lexer = ProcessYalp("./testsLabE/slr-1.yalp")

    

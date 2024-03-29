# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio C

from tree import Tree
from graphviz import Digraph
from rulesProcessing import processRules, createRulesDictionary

class Lexer:
    def __init__(self, filepath) -> None:
        self.lines = self.openFile(filepath)
        self.tokens = {}
        self.rules = {}
        self.createDictionary()

    def openFile(self, filepath="./testsLabC/slr-4.yal"):
        """ 
            Abrir archivo.
            Parámetos:
            - filename: Path relativo del archivo .yal
        
        """
        with open(filepath, "r") as f:
            lines = f.readlines()
        return lines

    def createDictionary(self):
        rulesList = []
        # Crear estructura de datos con tokens
        for pos, line in enumerate(self.lines):
            cleanLine = line.strip()
            # Si la línea comienza con "let"
            if cleanLine[:3] == "let":
                # Obtener el nombre del token
                token_name = line[line.index(" ")+1:line.index("=")].strip()
                
                # Obtener el valor del token
                tkn_value_start = line.index("=") + 1
                tkn_value_end = line.find("\n", tkn_value_start)
                tokenValue = line[tkn_value_start:tkn_value_end].strip()
                
                # Agregar token a diccionario
                self.tokens[token_name] = tokenValue
            
            elif cleanLine[:4] == "rule":
                rulesList = self.lines[pos:]

        for tokenName, tokenValue in self.tokens.items():

            if isinstance(tokenValue, list):
                new_value = []
                for c in tokenValue:
                    if c == "\n":
                        new_value.append("\n")
                    elif c == "\t":
                        new_value.append("\t")
                    else:
                        new_value.append(c)

                self.tokens[tokenName] = new_value

            if tokenValue[0:1] == ("[") and list(tokenValue)[-1] == ("]"):
                tokenValue = tokenValue[1:-1]

                tokenValue = tokenValue.replace("'", "")  # eliminar comillas simples
                tokenValue = tokenValue.replace('"', "")  # eliminar comillas simples
                tokenValue = tokenValue.replace("-", "")  # reemplazar guiones por barras verticales
                self.tokens[tokenName] = list(tokenValue)
                
                # Unir \\ con su respectivo char.
                for i in range(len(self.tokens[tokenName])):
                    if i < len(self.tokens[tokenName]):
                        if self.tokens[tokenName][i] == "\\":
                            self.tokens[tokenName][i] = self.tokens[tokenName][i] + self.tokens[tokenName][i+1]
                            self.tokens[tokenName].pop(i+1)

            # Leer casos donde esté un [] en otra parte del token y no tengan un -
            startIndex = 0
            endIndex = 0
            for i in range(len(tokenValue)):
                if tokenValue[i] == "[":
                    startIndex = i
                if tokenValue[i] == "]":
                    endIndex = i

            if (startIndex != 0 or endIndex != 0):
                tempList = list(tokenValue[startIndex+1:endIndex])
                # Unir comillas a valor
                i = 0 
                while i < len(tempList):
                    if i+2 < len(tempList) and tempList[i] == "'" and tempList[i+2] == "'":
                        tempList[i+1] = "'" + tempList[i+1] + "'"
                        tempList.pop(i)
                        tempList.pop(i+1)
                        # i = 
                    i = i + 1
                char_list = '|'.join(str(i) for i in tempList)
                tokenValue = tokenValue.replace(tokenValue[startIndex+1:endIndex], char_list)
                tokenValue = tokenValue.replace("[", '(')
                tokenValue = tokenValue.replace("]", ')')
                self.tokens[tokenName] = tokenValue

        # Añadir | para tokens en donde hayan []
        for tokenName, tokenValue in self.tokens.items():
            if all("\\" not in c for c in tokenValue) and isinstance(tokenValue, list):
                range_list = []    
                for i in range(0, len(tokenValue), 2):
                    range_list.extend(list(range(ord(tokenValue[i]), ord(tokenValue[i+1])+1)))
                char_list = '|'.join(chr(i) for i in range_list)
                self.tokens[tokenName] = char_list
            elif isinstance(tokenValue, list):
                char_list = '|'.join(str(i) for i in tokenValue)
                self.tokens[tokenName] = char_list

        # Sustituir tokenNames por tokenValue
        ids = sorted(self.tokens.keys(), key=len, reverse=True) # Ordenarlos para que busque primero las palabras más largas
        for tokenName, tokenValue in self.tokens.items():
            
            tokenValue = tokenValue.replace('.', "'.'")
            self.tokens[tokenName] = tokenValue

            newTokenValue = tokenValue
            for i in ids:
                if i in tokenValue:
                    # Sustituir el tokenName por self.tokens[tokenName], todo entre paréntesis
                    newTokenValue = newTokenValue.replace(i, "(" + str(self.tokens[i]) + ")")
                    self.tokens[tokenName] = newTokenValue

        # ------------------------------ Procesar rules ------------------------------ #
        strRules = processRules(rulesList)
        self.rules = createRulesDictionary(strRules)

        # Sustituir nombres de tokens por valor en rules
        for returnVal, tokenValue in self.rules.items():
            newTokenValue = tokenValue
            for i in ids:
                if i in tokenValue:
                    newTokenValue = newTokenValue.replace(i, "(" + str(self.tokens[i]) + ")")
                    self.rules[returnVal] = newTokenValue

        return self.rules

if __name__ == '__main__':

    # ------------------ Para mostrar árbol de tokens individuales ------------------ #

    lexer = Lexer("./testsLabC/slr-1.yal")
    # print(lexer.rules)
    posToken = 4
    tokenVal = list(lexer.rules.values())[posToken]
    tokenName = list(lexer.rules.keys())[posToken]

    tree = Tree(tokenVal, direct=True, tokenName=tokenName)
    tree = tree.tree
    treeTuple = tree.printNode()

    # Visualización de árbol
    graph = Digraph()
    tree.add_nodes(graph, treeTuple)
    graph.render('./treeImage/treeSingleToken', format='png', view=True)
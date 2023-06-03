import pprint
from LabC import Lexer
from LabE import ProcessYalp
from LR0 import LR0
from stack import Stack

class SLR1():

    def __init__(self, lr0: LR0) -> None:
        self.goto = {}
        self.action = {}
        self.lr0 = lr0
        self.states = {}
        self.getAbreviation = []
        self.productions = []
        self.createAbreviations()
        self.createProductionNum()
        self.gotoStr = []
        self.actionStr = []
        self.createTables()
        self.printTable()

    def createAbreviations(self):
        # Crear un diccionario con apodos de estados
        i = -1
        for state in self.lr0.states:
            i = i + 1
            stateNumber = 'S' + str(i)
            self.states[stateNumber] = state
            self.getAbreviation.append([state, stateNumber])
        
    def createProductionNum(self):
        self.productions = [(symbol, production[1:]) for symbol, production in self.lr0.productions]
        # print(self.productions.index(self.productions[2]))


    def createTables(self):
        # Crear diccionario
        for state in self.states.keys():
            subAction = {}
            for terminal in self.lr0.tokens:
                subAction[terminal] = []
            self.action[state] = subAction
        
        non_terminals = set([prod[0] for prod in self.lr0.productionRules])
        for state in self.states.keys():
            subGoTo = {}
            for non_terminal in non_terminals:
                subGoTo[non_terminal] = []
            self.goto[state] = subGoTo

        # Llenar tabla
        for transicion in self.lr0.transitions:
            at = transicion[0]
            inputV = transicion[1]
            to = transicion[2]

            # Ver cual es la abreviatura de at
            atAb = 0
            toAb = 0
            for ab in self.getAbreviation:
                both = False
                if ab[0] == at:
                    atAb = ab[1]
                if ab[0] == to:
                    toAb = ab[1]
                    
                if both:
                    break

            # Ver si toAb tiene el punto hasta el final

            # Calcular Action Reduce
            for dest in to:
                # Ver si tiene el punto hasta el final
                if dest[1][-1] == '.':
                    left = dest[0]
                    atFollow = self.lr0.follow[left]

                    # Buscar número
                    ogAt = (left, dest[1][:-1])
                    num = self.productions.index(ogAt)

                    # Llenar tabla
                    for i in atFollow:
                        self.action[atAb][i] = "R" + str(num)
                        strAction = f"{atAb} - ({i}) -> R{num}"
                        self.actionStr.append(strAction)

            # Añadir valores a GOTO y en Action añadir Shift
            if inputV in self.goto[atAb].keys():
                self.goto[atAb][inputV] = toAb
                strGoto = f"{atAb} - ({inputV}) -> {toAb}"
                self.gotoStr.append(strGoto)
            else:
                if inputV == '$':
                    self.action[atAb][inputV] = 'Accept'
                    strAction = f"{atAb} - ({inputV}) -> Accept"
                    self.actionStr.append(strAction)
                else:
                    self.action[atAb][inputV] = 'Shift ' + toAb[1:]
                    strAction = f"{atAb} - ({inputV}) -> Shift {toAb[1:]}"
                    self.actionStr.append(strAction)

    def printTable(self):
        # Imprimir tabla
        print('\nACTION')
        for state, dictI in self.action.items():
            for inputVal, action in dictI.items():
                strd = f"{state} - [{inputVal}] -> {action}"
                if action != []:
                    print(strd)

        
        print('\nGOTO')
        for state, dictI in self.goto.items():
            for inputVal, goto in dictI.items():
                strd = f"{state} - [{inputVal}] -> {goto}"
                if goto != []:
                    print(strd)

        print()

if __name__ == '__main__':

    filepath = "./testsLabC/slr-1.yal"
    filepathYalp = "./testsLabE/slr-1.yalp"
    lexer = Lexer(filepath)
    yalpProcess = ProcessYalp(filepathYalp)

    tokens = lexer.rules
    productions = yalpProcess.producciones

    lr0 = LR0(productions, tokens)
    slr1 = SLR1(lr0)
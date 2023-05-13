# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Archivo principal del programa

# Importar clases
from LabC import Lexer
from LabE import ProcessYalp
from LR0 import LR0

filepath = "./testsLabC/slr-1.yal"
filepathYalp = "./testsLabE/slr-1.yalp"
lexer = Lexer(filepath)
yalpProcess = ProcessYalp(filepathYalp)

tokens = lexer.rules
productions = yalpProcess.producciones

# Verificar que los tokens de yalpProcess estén definidos en el lexer
verifiedTokens = True
for token in yalpProcess.tokens:
    if token not in list(tokens.keys()):
        verifiedTokens = False

if verifiedTokens:
    lr = LR0(productions, tokens)
else:
    print('@! Error. Los tokens utilizados en el archivo .yalp no están totalmente definidos en el archivo .yal')
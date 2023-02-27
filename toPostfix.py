# Universidad del Valle de Guatemala
# Diseño de Lenguajes de Programación
# Ana Paola De León Molina, 20361
# Laboratorio A

# Módulo del algoritno Shunting para convertir la cadena de infix a postfix

def notGreater(val, stack):
    try:
        return True if val.precedence <= stack[-1].precedence else False
    except KeyError:
        return False

def toPostfix(regex, stack):
    '''
        Convierte una expresión regular infix a postfix.

        Parámetros:
        -----------
        - regex: Objeto stack con la regex contenida
        - stack: stack temporal para realizar la conversión
    '''

    regex = regex.item # Lista con valores de la regex
    output = []

    for val in regex: 

        if val.isNumeric == False:
            output.append(val) 
        
        elif val.value == '(': 
            stack.push(val) 

        elif val == ')': 

            while (not stack.isEmpty() and stack.peek().value != '('): 
                a = stack.pop() 
                output.append(a) 
            if (not stack.isEmpty() and stack.peek().value != '('): 
                return -1
            else: 
                stack.pop() 

        else: 
            while(not stack.isEmpty() and notGreater(val, regex)): 
                output.append(stack.pop()) 
            stack.push(val) 

    while not stack.isEmpty(): 
        output.append(stack.pop())

    print ("\n output", (output))
    print([(obj.value) for obj in output])
from lexer import lexer
from parser import Parser
from semantic import semantic_check  # si lo pusiste en otro archivo
from pprint import pprint
code = '''
scene inicio:
text "Estás en una cabaña."
choice "Salir" -> bosque
choice "Dormir" -> dormir

scene bosque:
text "Te dormís... Fin."

scene dormir:
text "Te dormís... Fin."
'''
tokens = lexer(code)
pprint(tokens)
parser = Parser(tokens)
ast = parser.parse()
print("\n Arbol de sintaxis abstracta (AST): ")
print(ast)

errores = semantic_check(ast)

if errores:
    print("\n Errores semánticos:")
    for e in errores:
        print("-", e)
else:
    print("\n Análisis semántico exitoso. Todo en orden.")

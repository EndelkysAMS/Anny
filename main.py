import sys
import antlr4
from antlr4 import FileStream, CommonTokenStream
from AnnyLexer import AnnyLexer
from AnnyParser import AnnyParser
from AnnyToJSCodeGenListener import AnnyToJSCodeGenListener   

def main():
    
    if len(sys.argv) != 2:
        print("Por favor, proporcione el archivo de entrada Anny.")
        sys.exit(1)

    
    input_file = sys.argv[1]

    input_stream = FileStream(input_file)

    # Crear un lexer y un parser
    lexer = AnnyLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = AnnyParser(token_stream)

    # Obtener el árbol de sintaxis (AST)
    tree = parser.programa()  

    
    with open("output.js", "w") as output_file:
        # Crear una instancia del listener
        listener = AnnyToJSCodeGenListener(output_file)
        
        walker = antlr4.ParseTreeWalker()
        walker.walk(listener, tree)

    print("El código JavaScript se ha generado correctamente en output.js")

if __name__ == '__main__':
    main()


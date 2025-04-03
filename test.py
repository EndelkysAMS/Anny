import sys
import antlr4
from antlr4 import FileStream, CommonTokenStream
from AnnyLexer import AnnyLexer
from AnnyParser import AnnyParser
from AnnyToJSCodeGenListener import AnnyToJSCodeGenListener
from SymbolTable import SymbolTable  
from ErrorTable import ErrorTable  
from io import StringIO  

def main():
    if len(sys.argv) != 2:
        print("Por favor, proporcione el archivo de entrada Anny.")
        sys.exit(1)

    input_file = sys.argv[1]
    input_stream = FileStream(input_file, encoding='utf-8') 

    
    lexer = AnnyLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = AnnyParser(token_stream)
    tree = parser.programa()

    
    print("\nÁrbol de sintaxis (AST):")
    print(tree.toStringTree(recog=parser)) 

    
    js_code_buffer = StringIO()
    
    
    symbol_table = SymbolTable()
    error_table = ErrorTable()
    listener = AnnyToJSCodeGenListener(
        output=js_code_buffer,  
        symbol_table=symbol_table,
        error_table=error_table
    )

    
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)

    print("\n=== Tabla de Errores ===")
    if error_table.errors:
        error_table.print_errors()
    else:
        print("No se encontraron errores.")

    print("\n=== Tabla de Símbolos ===")
    for nombre, tipo in symbol_table.symbols.items():
        print(f"{nombre}: {tipo}")

    
    error_table.print_errors()

    if not error_table.errors:
        
        with open("output.js", "w") as output_file:
            output_file.write(js_code_buffer.getvalue())
        print("\nEl código JavaScript se ha generado correctamente en output.js")
    else:
        print("\nHubo errores, no se generó el código JavaScript.")

if __name__ == '__main__':
    main()

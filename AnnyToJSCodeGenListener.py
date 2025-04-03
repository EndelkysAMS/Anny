import sys
from antlr4 import *
from AnnyLexer import AnnyLexer
from AnnyParser import AnnyParser
from AnnyListener import AnnyListener
from SymbolTable import SymbolTable  
from ErrorTable import ErrorTable  

class AnnyToJSCodeGenListener(AnnyListener):
    def __init__(self, output=None, symbol_table=None, error_table=None):
        self.output = output if output else sys.stdout
        self.indentCount = 0
        self.symbol_table = symbol_table if symbol_table else SymbolTable()
        self.error_table = error_table if error_table else ErrorTable()

    def _get_position(self, token):
        """Obtiene línea y columna ajustada (base 1)"""
        return (token.line, token.column + 1)

    def enterPrograma(self, ctx: AnnyParser.ProgramaContext):
        self.output.write("function main() {\n")
        self.indentCount += 1

    def exitPrograma(self, ctx: AnnyParser.ProgramaContext):
        self.indentCount -= 1
        self.output.write("}\n")

    def enterDeclaracion(self, ctx: AnnyParser.DeclaracionContext):
        variable_token = ctx.ID().symbol
        variable = variable_token.text
        tipo = ctx.getChild(0).getText()
        line, column = self._get_position(variable_token)
        
        if self.symbol_table.get_symbol(variable):
            self.error_table.add_error(100, 
                f"La variable '{variable}' ya está declarada", 
                line, column)
        else:
            self.symbol_table.add_symbol(variable, tipo)
        
        code_line = f"let {variable}"
        if ctx.expresion():
            code_line += f" = {ctx.expresion().getText()}"
        self.output.write(f"{'\t' * self.indentCount}{code_line};\n")

    def enterAsignacion(self, ctx: AnnyParser.AsignacionContext):
        variable_token = ctx.ID().symbol
        variable = variable_token.text
        line, column = self._get_position(variable_token)
        
        if not self.symbol_table.get_symbol(variable):
            self.error_table.add_error(200,
                f"Variable no declarada '{variable}'",
                line, column)
        
        self.output.write(f"{'\t' * self.indentCount}{variable} = {ctx.expresion().getText()};\n")

    def enterImprimir(self, ctx: AnnyParser.ImprimirContext):
        valores = [exp.getText() for exp in ctx.expresion()]
        self.output.write(f"{'\t' * self.indentCount}console.log({', '.join(valores)});\n")

    def enterLeer(self, ctx: AnnyParser.LeerContext):
        variable_token = ctx.ID().symbol
        variable = variable_token.text
        line, column = self._get_position(variable_token)
        
        if not self.symbol_table.get_symbol(variable):
            self.error_table.add_error(200,
                f"Variable no declarada '{variable}'",
                line, column)
        
        self.output.write(f"{'\t' * self.indentCount}let {variable} = prompt('Ingrese valor:');\n")

    def enterSi(self, ctx: AnnyParser.SiContext):
        self.output.write(f"{'\t' * self.indentCount}if ({ctx.expresion().getText()}) {{\n")
        self.indentCount += 1

    def exitSi(self, ctx: AnnyParser.SiContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")
        
        if ctx.bloque(1):
            self.output.write(f"{'\t' * self.indentCount}else {{\n")
            self.indentCount += 1

    def exitMientras(self, ctx: AnnyParser.MientrasContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")

    # ... (métodos restantes manteniendo misma estructura con manejo de errores)

def main():
    symbol_table = SymbolTable()
    error_table = ErrorTable()

    try:
        with open('output.js', 'w', encoding='utf-8') as output_file:
            input_stream = FileStream('example.anny', encoding='utf-8')
            lexer = AnnyLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = AnnyParser(stream)
            tree = parser.programa()
            
            listener = AnnyToJSCodeGenListener(
                output=output_file,
                symbol_table=symbol_table,
                error_table=error_table
            )
            
            walker = ParseTreeWalker()
            walker.walk(listener, tree)
            
    except Exception as e:
        error_table.add_error(999, f"Error inesperado: {str(e)}", 0, 0)
    
    finally:
        if error_table.errors:
            print("\n--- Errores encontrados ---")
            error_table.print_errors()
        else:
            print("\nTranspilación exitosa! Ver output.js")

if __name__ == "__main__":
    main()
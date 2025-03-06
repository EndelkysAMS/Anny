from antlr4 import *
from AnnyParser import AnnyParser
from AnnyListener import AnnyListener

class AnnyToJSCodeGenListener(AnnyListener) :
    def __init__(self, output):
        self.output = output
        self.indentCount = 0

    def enterPrograma(self, ctx: AnnyParser.ProgramaContext):
        self.output.write("function main() {\n")
        self.indentCount += 1

    def exitPrograma(self, ctx: AnnyParser.ProgramaContext):
        self.indentCount -= 1
        self.output.write("}\n")

    def enterDeclaracion(self, ctx: AnnyParser.DeclaracionContext):
        variable = ctx.ID().getText()
        if ctx.expresion():
            valor = ctx.expresion().getText()
            self.output.write(f"{'\t' * self.indentCount}let {variable} = {valor};\n")
        else:
            self.output.write(f"{'\t' * self.indentCount}let {variable};\n")

    def enterAsignacion(self, ctx: AnnyParser.AsignacionContext):
        variable = ctx.ID().getText()
        valor = ctx.expresion().getText()
        self.output.write(f"{'\t' * self.indentCount}{variable} = {valor};\n")

    def enterImprimir(self, ctx: AnnyParser.ImprimirContext):
        valores = [child.getText() for child in ctx.expresion()]
        self.output.write(f"{'\t' * self.indentCount}console.log({', '.join(valores)});\n")

    def enterLeer(self, ctx: AnnyParser.LeerContext):
        variable = ctx.ID().getText()
        self.output.write(f"{'\t' * self.indentCount}let {variable} = prompt('Enter value');\n")

    def enterSi(self, ctx: AnnyParser.SiContext):
        self.output.write(f"{'\t' * self.indentCount}if ({ctx.expresion().getText()}) {{\n")
        self.indentCount += 1

    def exitSi(self, ctx: AnnyParser.SiContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")

        if ctx.bloque(1):  # Verifica si hay un bloque 'sino'
            self.output.write(f"{'\t' * self.indentCount}else {{\n")
            self.indentCount += 1
            for child in ctx.bloque(1).getChildren():
                self.output.write(f"{'\t' * self.indentCount}{child.getText()}\n")
            self.indentCount -= 1
            self.output.write(f"{'\t' * self.indentCount}}}\n")

    def enterMientras(self, ctx: AnnyParser.MientrasContext):
        self.output.write(f"{'\t' * self.indentCount}while ({ctx.expresion().getText()}) {{\n")
        self.indentCount += 1

    def exitMientras(self, ctx: AnnyParser.MientrasContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")

    def enterPara(self, ctx: AnnyParser.ParaContext):
        variable = ctx.ID().getText()
        inicio = ctx.expresion(0).getText()
        fin = ctx.expresion(1).getText()
        paso = ctx.expresion(2).getText() if ctx.expresion(2) else '1'
        self.output.write(f"{'\t' * self.indentCount}for (let {variable} = {inicio}; {variable} <= {fin}; {variable} += {paso}) {{\n")
        self.indentCount += 1

    def exitPara(self, ctx: AnnyParser.ParaContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")

    def enterFuncion(self, ctx: AnnyParser.FuncionContext):
        func_name = ctx.ID().getText()
        params = ', '.join([param.getText() for param in ctx.parametros().ID()]) if ctx.parametros() else ''
        self.output.write(f"{'\t' * self.indentCount}function {func_name}({params}) {{\n")
        self.indentCount += 1

    def exitFuncion(self, ctx: AnnyParser.FuncionContext):
        self.indentCount -= 1
        self.output.write(f"{'\t' * self.indentCount}}}\n")

    def enterLlamadaFuncion(self, ctx: AnnyParser.LlamadaFuncionContext):
        func_name = ctx.ID().getText()
        if ctx.argumentos():
            args = ', '.join([arg.getText() for arg in ctx.argumentos().expresion()])
        else:
            args = ''
        self.output.write(f"{'\t' * self.indentCount}{func_name}({args});\n")

def enterRetorno(self, ctx: AnnyParser.RetornoContext):
    valor = ctx.expresion(0).getText() 
    self.output.write(f"{'\t' * self.indentCount}return {valor};\n")
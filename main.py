import sys
import os
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl 
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QMainWindow, QTextEdit, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QTabWidget, QMenuBar, 
                            QMenu, QTreeWidget, QTreeWidgetItem, QStatusBar, 
                            QFileDialog)
from PyQt6.QtGui import QDesktopServices
from AnnyLexer import AnnyLexer
from AnnyParser import AnnyParser
from SymbolTable import SymbolTable
from ErrorTable import ErrorTable
from AnnyToJSCodeGenListener import AnnyToJSCodeGenListener
from io import StringIO

class AnnyTranspilerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.error_table = ErrorTable()
        self.initUI()
        self.connect_signals()
        self.load_styles()

    def load_styles(self):
        if os.path.exists('styles.css'):
            with open('styles.css', 'r') as file:
                self.setStyleSheet(file.read())

    def initUI(self):
        self.setWindowTitle("Anny - Universidad Valle del Momboy")
        self.setGeometry(100, 100, 1200, 800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        
        menu_uvm = QMenu("Universidad Valle Del Momboy", self)
        menu_docs = QMenu("Documentación", self)
        menu_ejemplos = QMenu("Ejemplos", self)
        
        self.add_documentation_actions(menu_docs)
        menu_ejemplos.addAction("Ejemplo Básico", self.show_basic_examples)
        menu_ejemplos.addAction("Ejemplo Intermedio", self.show_intermediate_examples)
        menu_ejemplos.addAction("Ejemplo Avanzado", self.show_advanced_examples)
        
        menu_bar.addMenu(menu_uvm)
        menu_bar.addMenu(menu_docs)
        menu_bar.addMenu(menu_ejemplos)

        header_label = QLabel("Lenguaje Anny\n\nEstudiantes: Zeuddy Segovia y Endelkys Matos  |  Profesora: Katiuska Morillo")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        code_layout = QHBoxLayout()
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Ingrese su código Anny aquí...")
        code_layout.addWidget(self.create_section("Código Fuente", self.code_input))
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        code_layout.addWidget(self.create_section("Salida en JavaScript", self.output_area))
        main_layout.addLayout(code_layout)

        self.tab_widget = QTabWidget()
        self.token_table = self.create_table(["Tipo", "Valor", "Línea", "Columna"])
        self.ast_tree = self.create_ast_tree()
        self.symbol_table_widget = self.create_table(["Nombre", "Tipo", "Ámbito"])
        self.error_table_widget = self.create_table(["Tipo", "Mensaje", "Línea", "Columna"])
        
        self.tab_widget.addTab(self.token_table, "Tokens")
        self.tab_widget.addTab(self.ast_tree, "AST")
        self.tab_widget.addTab(self.symbol_table_widget, "Tabla de Símbolos")
        self.tab_widget.addTab(self.error_table_widget, "Errores")
        main_layout.addWidget(self.tab_widget)

        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Ejecutar Compilador")
        self.download_button = QPushButton("Descargar JS")
        self.clear_button = QPushButton("Limpiar")
        
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def add_documentation_actions(self, menu):
        doc_actions = [
            ("Manual de Sintaxis", "sintaxis.pdf"),
            ("Tabla de Símbolos", "simbolos.pdf"),
            ("Manejo de Errores", "errores.pdf")
        ]
        
        for text, filename in doc_actions:
            menu.addAction(text, lambda checked, f=filename: self.download_document(f))

    def download_document(self, filename):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar documento", filename, "PDF Files (*.pdf)", options=options)
        
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pass
                self.status_bar.showMessage(f"Documento {filename} guardado exitosamente", 5000)
            except Exception as e:
                self.status_bar.showMessage(f"Error al guardar: {str(e)}", 5000)

    def show_basic_examples(self):
        example_code = """
inicio  
  entero x = 10;  
  decimal y = 5.5;  
  cadena mensaje = "Hola, mundo";  
  imprimir(x, y, mensaje);  
fin  

"""
        self.code_input.setPlainText(example_code)

    def show_intermediate_examples(self):
        example_code = """"
   
    inicio  
  entero num;  
  leer(num);  

  si (num > 10) entonces  
    imprimir("El número es mayor a 10");  
  sino  
    imprimir("El número es menor o igual a 10");  
  fin_si  
fin  

"""
        self.code_input.setPlainText(example_code)

    def show_advanced_examples(self):
        example_code = """
    inicio  
  funcion factorial(n) hacer  
    entero resultado = 1;  
    mientras (n > 1) hacer  
      resultado = resultado * n;  
      n = n - 1;  
    fin_mientras  
    retorna resultado;  
  fin_funcion  

  entero num;  
  leer(num);  
  entero fact = factorial(num);  
  imprimir("El factorial es:", fact);  
fin  
"""
        self.code_input.setPlainText(example_code)

    def connect_signals(self):
        self.run_button.clicked.connect(self.run_transpiler)
        self.download_button.clicked.connect(self.download_js)
        self.clear_button.clicked.connect(self.clear_all)

    def create_section(self, title, widget):
        section = QWidget()
        layout = QVBoxLayout()
        label = QLabel(title)
        layout.addWidget(label)
        layout.addWidget(widget)
        section.setLayout(layout)
        return section

    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        return table

    def create_ast_tree(self):
        tree = QTreeWidget()
        tree.setHeaderLabel("Árbol de Sintaxis Abstracta (AST)")
        tree.setColumnCount(1)
        return tree

    def run_transpiler(self):
        code = self.code_input.toPlainText()
        if not code.strip():
            self.status_bar.showMessage("Error: El código de entrada está vacío", 5000)
            return

        self.clear_results()

        try:
            input_stream = InputStream(code)
            lexer = AnnyLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = AnnyParser(stream)
            tree = parser.programa()

            self.process_tokens(lexer)
            self.build_ast(tree)
            self.generate_js_code(tree)
            self.update_tables()

            if self.error_table.errors:
                self.status_bar.showMessage("Compilación completada con errores", 5000)
            else:
                self.status_bar.showMessage("Compilación exitosa", 5000)

        except Exception as e:
            self.error_table.add_error(999, f"Error de ejecución: {str(e)}", 0, 0)
            self.update_tables()
            self.status_bar.showMessage(f"Error crítico: {str(e)}", 5000)

    def process_tokens(self, lexer):
        tokens = []
        lexer.reset()
        for token in lexer.getAllTokens():
            if token.type == Token.EOF:
                continue
                
            token_name = lexer.symbolicNames[token.type] 
            tokens.append([
                token_name,
                token.text,
                str(token.line),
                str(token.column + 1)
            ])

        self.token_table.setRowCount(len(tokens))
        for row, token_data in enumerate(tokens):
            for col, data in enumerate(token_data):
                self.token_table.setItem(row, col, QTableWidgetItem(data))

    def build_ast(self, tree):
        self.ast_tree.clear()
        root_node = self.create_ast_node(tree)
        self.ast_tree.addTopLevelItem(root_node)
        self.ast_tree.expandAll()

    def create_ast_node(self, node):
        if isinstance(node, TerminalNodeImpl):
            token = node.getSymbol()
            try:
                token_name = AnnyLexer.symbolicNames[token.type]
            except IndexError:
                token_name = f"TKN_{token.type}"
            return QTreeWidgetItem([f"{token_name}: {token.text}"])
        
        try:
            rule_index = node.getRuleIndex()
            if rule_index < len(AnnyParser.ruleNames):
                rule_name = AnnyParser.ruleNames[rule_index]
            else:
                rule_name = f"AnonymousRule_{rule_index}"
            
            item = QTreeWidgetItem([rule_name])
            
            for i in range(node.getChildCount()):
                child = node.getChild(i)
                if child is not None:
                    item.addChild(self.create_ast_node(child))
            
            return item
        
        except Exception as e:
            return QTreeWidgetItem([f"ERROR: {str(e)}"])

    def generate_js_code(self, tree):
        js_buffer = StringIO()
        listener = AnnyToJSCodeGenListener(
            output=js_buffer,
            symbol_table=self.symbol_table,
            error_table=self.error_table
        )
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        self.output_area.setPlainText(js_buffer.getvalue())

    def update_tables(self):
        self.symbol_table_widget.setRowCount(len(self.symbol_table.symbols))
        for row, (name, symbol) in enumerate(self.symbol_table.symbols.items()):
            self.symbol_table_widget.setItem(row, 0, QTableWidgetItem(name))
            self.symbol_table_widget.setItem(row, 1, QTableWidgetItem(symbol.type))
            self.symbol_table_widget.setItem(row, 2, QTableWidgetItem(symbol.scope))

        self.error_table_widget.setRowCount(len(self.error_table.errors))
        for row, error in enumerate(self.error_table.errors):
            self.error_table_widget.setItem(row, 0, QTableWidgetItem(str(error['error_code'])))
            self.error_table_widget.setItem(row, 1, QTableWidgetItem(error['message']))
            self.error_table_widget.setItem(row, 2, QTableWidgetItem(str(error['line'])))
            self.error_table_widget.setItem(row, 3, QTableWidgetItem(str(error['column'])))

    def download_js(self):
        js_code = self.output_area.toPlainText()
        if not js_code.strip():
            self.status_bar.showMessage("No hay código JavaScript para guardar", 5000)
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar JavaScript", "", "JavaScript Files (*.js)", options=options)
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(js_code)
                self.status_bar.showMessage(f"Archivo guardado: {file_path}", 5000)
            except Exception as e:
                self.status_bar.showMessage(f"Error al guardar: {str(e)}", 5000)

    def clear_results(self):
        self.output_area.clear()
        self.token_table.setRowCount(0)
        self.ast_tree.clear()
        self.symbol_table_widget.setRowCount(0)
        self.error_table_widget.setRowCount(0)
        self.symbol_table = SymbolTable()
        self.error_table = ErrorTable()

    def clear_all(self):
        self.code_input.clear()
        self.clear_results()
        self.status_bar.clearMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnnyTranspilerApp()
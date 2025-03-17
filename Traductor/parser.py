class ParserError(Exception):
    """Excepción para errores sintácticos con contexto"""
    def __init__(self, message, token=None):
        error_msg = f"[SINTÁCTICO] {message}"
        if token:
            error_msg += f" en línea {token.line}, columna {token.column}"
        super().__init__(error_msg)

class Parser:
    """Implementa un parser recursivo descendente para expresiones complejas"""
    
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.advance()
    
    def advance(self):
        """Avanza al siguiente token"""
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None
    
    def expect(self, expected_type):
        """Verifica y consume un token específico"""
        if self.current_token and self.current_token.type == expected_type:
            self.advance()
        else:
            found = self.current_token.type if self.current_token else "EOF"
            raise ParserError(f"Se esperaba '{expected_type}' pero se encontró '{found}'", self.current_token)
    
    def parse(self):
        """Punto de entrada principal del análisis"""
        self.program()
        if self.current_token and self.current_token.type != 'EOF':
            raise ParserError("Caracteres adicionales inesperados", self.current_token)
    
    def program(self):
        """Regla: program → 'program' ID '{' block '}'"""
        self.expect('PROGRAM')
        self.expect('ID')
        self.expect('LBRACE')
        self.block()
        self.expect('RBRACE')
    
    def block(self):
        """Regla: block → (declaration | statement)*"""
        while self.current_token and self.current_token.type in ['VAR', 'ID', 'PRINT']:
            if self.current_token.type == 'VAR':
                self.declaration()
            else:
                self.statement()
    
    def declaration(self):
        """Regla: declaration → 'var' ID ':' type ';'"""
        self.expect('VAR')
        self.expect('ID')
        self.expect('COLON')
        self.type_()
        self.expect('SEMI')
    
    def type_(self):
        """Regla: type → 'int' | 'float' | 'string'"""
        valid_types = ['INT', 'FLOAT', 'STRING']
        if self.current_token.type in valid_types:
            self.expect(self.current_token.type)
        else:
            raise ParserError("Tipo no válido", self.current_token)
    
    def statement(self):
        """Regla: statement → assignment | print_statement"""
        if self.current_token.type == 'ID':
            self.assignment()
        elif self.current_token.type == 'PRINT':
            self.print_statement()
        else:
            raise ParserError("Sentencia no reconocida", self.current_token)
    
    def assignment(self):
        """Regla: assignment → ID '=' expr ';'"""
        self.expect('ID')
        self.expect('ASSIGN')
        self.expr()
        self.expect('SEMI')
    
    def print_statement(self):
        """Regla: print_statement → 'print' '(' expr ')' ';'"""
        self.expect('PRINT')
        self.expect('LPAREN')
        self.expr()
        self.expect('RPAREN')
        self.expect('SEMI')
    
    def expr(self):
        """Regla: expr → term (OP term)*"""
        self.term()
        # Manejar múltiples operaciones: 1 + 2 * 3 - 4
        while self.current_token and self.current_token.type == 'OP':
            self.expect('OP')
            self.term()
    
    def term(self):
        """Regla: term → ID | NUMBER | STRING | '(' expr ')'"""
        if self.current_token.type in ['ID', 'NUMBER', 'STRING']:
            self.advance()
        elif self.current_token.type == 'LPAREN':
            self.expect('LPAREN')
            self.expr()  # Llamada recursiva para expresiones anidadas
            self.expect('RPAREN')
        else:
            raise ParserError("Término no válido", self.current_token)
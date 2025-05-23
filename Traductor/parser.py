from collections import namedtuple

class ParserError(Exception):
    def __init__(self, message, token):
        super().__init__(message)
        self.token = token

class Parser:
    friendly_names = {
        'ID': 'identificador',
        'OP': 'operador',
        'SEMI': 'punto y coma',
        'LPAREN': 'paréntesis izquierdo "("',
        'RPAREN': 'paréntesis derecho ")"',
        'LBRACE': 'llave izquierda "{"',
        'RBRACE': 'llave derecha "}"',
        'COMMA': 'coma ","',
        'ASSIGN': 'signo de asignación "="',
        'PROGRAM': 'palabra reservada "program"',
        'INT': 'tipo entero',
        'FLOAT': 'tipo flotante',
        'STRING': 'tipo cadena',
        'NUMBER': 'número',
        'EOF': 'fin de archivo',
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.errors = []

    def friendly(self, token_type):
        return self.friendly_names.get(token_type, token_type.lower())

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = namedtuple('Token', ['type', 'value', 'line', 'column'])('EOF', '', self.current_token.line, self.current_token.column)

    def expect(self, expected_type):
        found = self.current_token.type
        if found == expected_type:
            self.advance()
        else:
            exp_friendly = self.friendly(expected_type)
            found_friendly = self.friendly(found)
            msg = f"[SINTÁCTICO] Se esperaba {exp_friendly} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

    def parse(self):
        try:
            if self.current_token.type == 'PROGRAM':
                self.program_with_program_keyword()
            else:
                self.program_c_style()
        except ParserError:
            # Captura para seguir mostrando otros errores
            pass

    def program_with_program_keyword(self):
        self.expect('PROGRAM')
        self.expect('ID')      # Nombre programa
        self.expect('LPAREN')
        self.expect('RPAREN')
        self.expect('LBRACE')
        self.statements()
        self.expect('RBRACE')
        self.expect('EOF')

    def program_c_style(self):
        while self.current_token.type != 'EOF':
            try:
                self.function_or_declaration()
            except ParserError:
                self.advance()

    def function_or_declaration(self):
        if self.current_token.type in ('INT', 'FLOAT', 'STRING'):
            self.advance()
        else:
            expected = "tipo (int, float, string)"
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

        self.expect('ID')

        if self.current_token.type == 'LPAREN':
            self.function_definition()
        elif self.current_token.type == 'SEMI':
            self.advance()
        else:
            expected = 'paréntesis izquierdo "(" o punto y coma ";"'
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

    def function_definition(self):
        self.expect('LPAREN')
        self.parameter_list()
        self.expect('RPAREN')
        self.expect('LBRACE')
        self.statements()
        self.expect('RBRACE')

    def parameter_list(self):
        if self.current_token.type in ('INT', 'FLOAT', 'STRING'):
            self.parameter()
            while self.current_token.type == 'COMMA':
                self.advance()
                self.parameter()

    def parameter(self):
        if self.current_token.type in ('INT', 'FLOAT', 'STRING'):
            self.advance()
            self.expect('ID')
        else:
            expected = "tipo para parámetro"
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

    def statements(self):
        while self.current_token.type not in ('RBRACE', 'EOF'):
            try:
                self.statement()
            except ParserError:
                self.advance()

    def statement(self):
        if self.current_token.type in ('INT', 'FLOAT', 'STRING'):
            self.variable_declaration()
        elif self.current_token.type == 'ID':
            self.assignment_or_function_call()
        else:
            expected = "declaración o instrucción"
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

    def variable_declaration(self):
        self.advance()
        self.expect('ID')
        self.expect('SEMI')

    def assignment_or_function_call(self):
        id_token = self.current_token
        self.advance()
        if self.current_token.type == 'ASSIGN':
            self.advance()
            self.expression()
            self.expect('SEMI')
        elif self.current_token.type == 'LPAREN':
            self.function_call()
            self.expect('SEMI')
        else:
            expected = "signo de asignación '=' o paréntesis izquierdo '('"
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} después de identificador pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

    def function_call(self):
        self.expect('LPAREN')
        self.argument_list()
        self.expect('RPAREN')

    def argument_list(self):
        if self.current_token.type not in ('RPAREN',):
            self.expression()
            while self.current_token.type == 'COMMA':
                self.advance()
                self.expression()

    def expression(self):
        if self.current_token.type == 'ID':
            self.advance()
            if self.current_token.type == 'LPAREN':
                self.function_call()
        elif self.current_token.type == 'NUMBER':
            self.advance()
        else:
            expected = "expresión"
            found_friendly = self.friendly(self.current_token.type)
            msg = f"[SINTÁCTICO] Se esperaba {expected} pero se encontró {found_friendly} en línea {self.current_token.line}, columna {self.current_token.column}"
            self.errors.append(msg)
            raise ParserError(msg, self.current_token)

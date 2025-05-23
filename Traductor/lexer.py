import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self):
        self.text = ''
        self.pos = 0
        self.line = 1
        self.column = 1
        self.token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),      # Enteros o flotantes
            ('ID',       r'[A-Za-z_]\w*'),     # Identificadores
            ('ASSIGN',   r'='),                # Asignación =
            ('SEMI',     r';'),                # Punto y coma
            ('LPAREN',   r'\('),               # Paréntesis izquierdo
            ('RPAREN',   r'\)'),               # Paréntesis derecho
            ('LBRACE',   r'\{'),               # Llave izquierda
            ('RBRACE',   r'\}'),               # Llave derecha
            ('COLON',    r':'),                # Dos puntos
            ('COMMA',    r','),                # Coma
            ('OP',       r'[+\-*/]'),          # Operadores aritméticos
            ('NEWLINE',  r'\n'),               # Nueva línea
            ('SKIP',     r'[ \t]+'),           # Espacios y tabs (se ignoran)
            ('STRING',   r'"[^"\n]*"'),        # Cadenas entre comillas dobles
            ('MISMATCH', r'.'),                # Cualquier otro carácter no válido
        ]
        self.keywords = {
            'var': 'VAR',
            'int': 'INT',
            'float': 'FLOAT',
            'string': 'STRING',
            'print': 'PRINT',
            'program': 'PROGRAM',
        }
        self.regex = re.compile('|'.join(
            f'(?P<{name}>{pattern})' for name, pattern in self.token_specification
        ))

    def tokenize(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1

        for mo in self.regex.finditer(self.text):
            kind = mo.lastgroup
            raw_value = mo.group()
            value = raw_value

            if kind == 'NUMBER':
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            elif kind == 'ID':
                kind = self.keywords.get(value, 'ID')
            elif kind == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            elif kind == 'SKIP':
                self.column += len(value)
                continue
            elif kind == 'MISMATCH':
                raise LexerError(f'Error léxico: Carácter inesperado {value!r} en línea {self.line}, columna {self.column}')

            yield Token(kind, value, self.line, self.column)
            self.column += len(raw_value)

        yield Token('EOF', '', self.line, self.column)

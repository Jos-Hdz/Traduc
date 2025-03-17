import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class LexerError(Exception):
    """Maneja errores léxicos con ubicación precisa"""
    def __init__(self, message, line, column):
        super().__init__(f"[LÉXICO] {message} en línea {line}, columna {column}")
        self.line = line
        self.column = column

class Lexer:
    keywords = {
        'program', 'var', 'int', 'float', 'string',
        'if', 'else', 'print'
    }
    
    # Orden crítico: tokens más específicos primero
    tokens = [
        ('COMMENT', r'//.*'),
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+(\.\d*)?'),
        ('EQ', r'=='),
        ('ASSIGN', r'='),
        ('COLON', r':'),
        ('SEMI', r';'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('OP', r'[+\-*/]'),  # Operadores aritméticos
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('WHITESPACE', r'\s+')
    ]
    
    def __init__(self):
        self._tokens_re = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.tokens),
            re.MULTILINE
        )
    
    def tokenize(self, code):
        """Convierte código fuente en tokens con tracking de posición"""
        line_num = 1
        line_start = 0
        pos = 0
        
        while pos < len(code):
            match = self._tokens_re.match(code, pos)
            if match:
                kind = match.lastgroup
                value = match.group(kind)
                column = match.start() - line_start
                
                if kind == 'WHITESPACE':
                    if '\n' in value:
                        line_num += value.count('\n')
                        line_start = match.end()
                    pos = match.end()
                    continue
                elif kind == 'COMMENT':
                    pos = match.end()
                    continue
                
                if kind == 'ID' and value in self.keywords:
                    kind = value.upper()
                
                yield Token(kind, value, line_num, column + 1)
                pos = match.end()
            else:
                char = code[pos]
                raise LexerError(f"Carácter inválido: '{char}'", line_num, pos - line_start + 1)
        
        yield Token('EOF', '', line_num, pos - line_start + 1)
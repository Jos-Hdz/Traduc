import re

def lexer(code):
    # Definir las expresiones regulares para cada token
    token_specifications = [
        ("ID", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),  # Identificadores
        ("NUMBER", r"\d+(\.\d+)?"),             # Números (enteros y reales)
        ("STRING", r'"[^"]*"'),                 # Cadenas
        ("TYPE", r"\b(int|float|string)\b"),    # Tipos
        ("OP", r"[+\-*/]|==|<=|>=|<|>|="),      # Operadores
        ("LOGIC", r"\b(or|and|not)\b"),         # Operadores lógicos
        ("SYMBOL", r"[;,()\{\}]"),              # Símbolos
        ("KEYWORD", r"\b(if|while|return|else)\b"),  # Palabras clave
        ("EOF", r"\$"),                         # Fin de entrada
        ("WHITESPACE", r"\s+"),                 # Espacios en blanco (ignorar)
    ]

    # Compilar patrones
    token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specifications)
    regex_compiled = re.compile(token_regex)
    tokens = []

    # Tokenizar el código fuente
    for match in regex_compiled.finditer(code):
        token_type = match.lastgroup
        token_value = match.group()
        if token_type != "WHITESPACE":  # Ignorar espacios
            tokens.append((token_type, token_value))

    return tokens

# Ejemplo de uso
codigo = """
int x = 10;
if (x > 5) {
    return x + 1;
} else {
    return 0;
} $
"""

tokens = lexer(codigo)
print(tokens)

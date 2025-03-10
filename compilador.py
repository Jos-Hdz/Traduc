import re

# ------------------------------
# Analizador Léxico
# ------------------------------
def lexer(code):
    token_specifications = [
        ("TYPE", r"\b(int|float|string)\b"),
        ("KEYWORD", r"\b(if|while|return|else)\b"),
        ("OPRELAC", r"<=|>=|<|>"),
        ("OPIGUALDAD", r"=="),
        ("OPSUMA", r"\+|-"),
        ("OPMUL", r"\*|/"),
        ("LOGIC_OR", r"\bor\b"),
        ("LOGIC_AND", r"\band\b"),
        ("LOGIC_NOT", r"\bnot\b"),
        ("ASIGNACION", r"="),
        ("SYMBOL", r";|,|\(|\)|{|}"),
        ("ENTERO", r"\d+"),
        ("REAL", r"\d+\.\d+"),
        ("CADENA", r'"[^"]*"'),
        ("ID", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
        ("EOF", r"\$"),
        ("WHITESPACE", r"\s+"),
    ]

    tokens = []
    for match in re.finditer(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specifications), code
    ):
        token_type = match.lastgroup
        token_value = match.group()
        if token_type == "WHITESPACE":
            continue
        tokens.append((token_type, token_value))
    
    if not tokens or tokens[-1][0] != "EOF":
        tokens.append(("EOF", "$"))
    return tokens

# ------------------------------
# Mapeo de Tokens a Códigos
# ------------------------------
token_map = {
    "ID": 0,
    "ENTERO": 1,
    "REAL": 2,
    "CADENA": 3,
    "TYPE": 4,
    "OPSUMA": 5,
    "OPMUL": 6,
    "OPRELAC": 7,
    "LOGIC_OR": 8,
    "LOGIC_AND": 9,
    "LOGIC_NOT": 10,
    "OPIGUALDAD": 11,
    "SYMBOL": lambda v: 12 if v == ";" else 13 if v == "," else 14 if v == "(" else 15 if v == ")" else 16 if v == "{" else 17,
    "ASIGNACION": 18,
    "KEYWORD": lambda v: 19 if v == "if" else 20 if v == "while" else 21 if v == "return" else 22,
    "EOF": 23,
}

def translate_tokens(tokens):
    translated = []
    for token_type, value in tokens:
        if token_type == "SYMBOL":
            translated.append(token_map["SYMBOL"](value))
        elif token_type == "KEYWORD":
            translated.append(token_map["KEYWORD"](value))
        else:
            translated.append(token_map[token_type])
    return translated

# ------------------------------
# Analizador Sintáctico LR
# ------------------------------
def load_grammar(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    # Leer producciones
    num_productions = int(lines[0])
    productions = []
    for line in lines[1:num_productions + 1]:
        parts = line.split('\t')
        lhs = int(parts[0])
        rhs_len = int(parts[1])
        productions.append((lhs, rhs_len))
    
    # Leer estados y tablas
    state_line = lines[num_productions + 1].split('\t')
    num_states = int(state_line[0])
    num_symbols = int(state_line[1])
    
    action_table = []
    goto_table = []
    for line in lines[num_productions + 2:]:
        entries = list(map(int, line.split('\t')))
        action = entries[:24]
        goto = entries[24:24 + 22]
        action_table.append(action)
        goto_table.append(goto)
    
    return productions, action_table, goto_table

def parse(tokens, productions, action_table, goto_table):
    stack = [0]
    token_index = 0
    current_token = tokens[token_index] if tokens else 23
    
    while True:
        state = stack[-1]
        action = action_table[state][current_token]
        
        if action > 0:  # Desplazar
            stack.append(current_token)
            stack.append(action)
            token_index += 1
            if token_index < len(tokens):
                current_token = tokens[token_index]
            else:
                current_token = 23  # EOF
        elif action < 0:  # Reducir
            prod_num = -action
            lhs, rhs_len = productions[prod_num - 1]
            stack = stack[:-2 * rhs_len]
            state = stack[-1]
            goto_state = goto_table[state][lhs - 24]  # No terminales empiezan en 24
            stack.append(lhs)
            stack.append(goto_state)
        elif action == 0:  # Error
            raise SyntaxError(f"Error de sintaxis en token {current_token}")
        else:  # Aceptar
            if current_token == 23 and len(stack) == 2 and stack[0] == 0 and stack[1] == 24:
                print("\n¡Análisis exitoso! La entrada es válida.")
                return True
            else:
                raise SyntaxError("Error: entrada no válida después de EOF")

# ------------------------------
# Ejemplo de Uso
# ------------------------------
if __name__ == "__main__":
    # Cargar gramática y tablas LR
    productions, action_table, goto_table = load_grammar("compilador.Ir")
    
    # Código de entrada
    code = """
        int x = 10;
        if (x > 5) {
            return x;
        } $
    """
    
    # Ejecutar lexer y traducir tokens
    tokens = lexer(code)
    print("Tokens generados:", tokens)
    token_codes = translate_tokens(tokens)
    print("Códigos de tokens:", token_codes)
    
    # Ejecutar parser
    try:
        parse(token_codes, productions, action_table, goto_table)
    except SyntaxError as e:
        print(f"\nError de sintaxis: {e}")
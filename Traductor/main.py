from lexer import Lexer, LexerError
from parser import Parser, ParserError
import sys

def main():
    """Coordinador principal del proceso de análisis"""
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo_fuente>")
        print("Ejemplo: python main.py ejemplos/operaciones.src")
        return
    
    try:
        with open(sys.argv[1]) as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Error: Archivo '{sys.argv[1]}' no encontrado")
        return
    
    # Análisis léxico
    lexer = Lexer()
    try:
        tokens = list(lexer.tokenize(codigo))
    except LexerError as e:
        print(f"\n{str(e)}")
        return
    
    # Análisis sintáctico
    try:
        parser = Parser(tokens)
        parser.parse()
        print("\n[ÉXITO] Análisis completado correctamente")
    except ParserError as e:
        print(f"\n{str(e)}")

if __name__ == "__main__":
    main()
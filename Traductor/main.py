from lexer import Lexer, LexerError
from parser import Parser
import sys

def main():
    """Coordinador principal del proceso de análisis"""
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo_fuente>")
        print("Ejemplo: python main.py ejemplos/operaciones.src")
        return

    try:
        with open(sys.argv[1], encoding='utf-8') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Error: Archivo '{sys.argv[1]}' no encontrado")
        return

    # Análisis léxico
    lexer = Lexer()  # ✅ Sin argumentos
    try:
        tokens = list(lexer.tokenize(codigo))  # ✅ Aquí se pasa el texto fuente
    except LexerError as e:
        print(f"\n[ERROR LÉXICO]: {str(e)}")
        return

    # Análisis sintáctico
    parser = Parser(tokens)
    parser.parse()

    # Mostrar errores encontrados
    if parser.errors:
        print("\n[ERRORES ENCONTRADOS]:")
        for error in parser.errors:
            print(f"- {error}")
    else:
        print("\n[ÉXITO] Análisis completado correctamente")

if __name__ == "__main__":
    main()

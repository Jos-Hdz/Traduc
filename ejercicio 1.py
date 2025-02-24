class Lexico:
    def __init__(self, cadena):
        self.cadena = cadena
        self.pos = 0
        self.tokens = []
    
    def analisis_lexico(self):
        while self.pos < len(self.cadena):
            char = self.cadena[self.pos]
            
            if char.isalpha():  # Identificador (agrupar múltiples letras)
                inicio = self.pos
                while self.pos < len(self.cadena) and self.cadena[self.pos].isalpha():
                    self.pos += 1
                self.tokens.append(0)  # Un solo token por identificador
                
            elif char == '+':  # Operador
                self.tokens.append(1)
                self.pos += 1
                
            else:  # Carácter no válido
                raise ValueError(f"Carácter no reconocido: {char}")
                
        self.tokens.append(2)  # Fin de cadena ($)
        return self.tokens

# El resto del código del parser se mantiene igual
class ParserLR:
    def __init__(self):
        self.tabla = {
            0: {0: ('d', 2),    1: None,       2: None,       'E': 1},
            1: {0: ('r', 0),    1: ('r', 0),   2: ('acc',)},  # Aceptación
            2: {0: None,        1: ('d', 3),   2: None,       'E': None},
            3: {0: ('d', 4),    1: None,       2: None,       'E': None},
            4: {0: ('r', 1),    1: ('r', 1),   2: ('r', 1),   'E': None}
        }
        self.producciones = [('E', 3)]  # E -> id + id

    def parse(self, tokens):
        pila = [0]
        cursor = 0
        
        while True:
            estado = pila[-1]
            actual = tokens[cursor] if cursor < len(tokens) else 2
            
            accion = self.tabla[estado].get(actual, None)
            
            if not accion:
                print("Error: Cadena no válida")
                return False
                
            if accion[0] == 'd':    # Desplazamiento
                pila.append(actual)
                pila.append(accion[1])
                cursor += 1
            elif accion[0] == 'r':  # Reducción
                prod = self.producciones[accion[1]-1]
                for _ in range(2 * prod[1]):  # Pop de símbolos
                    pila.pop()
                estado_actual = pila[-1]
                pila.append('E')
                pila.append(self.tabla[estado_actual]['E'])
            elif accion[0] == 'acc': # Aceptación
                print("Cadena válida!")
                return True

# Ejecución con "hola+mundo"
entrada = "hola+mundo"

try:
    lex = Lexico(entrada)
    tokens = lex.analisis_lexico()
    print(f"Tokens generados para '{entrada}': {tokens}")
    
    parser = ParserLR()
    parser.parse(tokens)
except ValueError as e:
    print(f"Error léxico: {e}")
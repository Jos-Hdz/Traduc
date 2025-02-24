# Tabla LR(1)
tabla = [
    [2, -1, 1],  # Estado 0
    [-1, -1, 0],  # Estado 1 (aceptación)
    [3, -2, -1],  # Estado 2
    [2, -1, 4],  # Estado 3
    [-1, -1, -1]  # Estado 4
]

# Reglas de producción
id_reglas = [2, 2]  # Ambos producen E
lon_reglas = [3, 1]  # Longitudes de las reglas

# Simbolos de entrada (id → 0, + → 1, $ → 2)
entrada = [0, 1, 0, 2]  # Representación de "id + id $"

# Pilas
pila_estados = [0]
pila_simbolos = [-1]  # -1 representa el símbolo inicial
pos = 0  # Puntero a la entrada

while True:
    estado_actual = pila_estados[-1]
    simbolo_actual = entrada[pos]

    accion = tabla[estado_actual][simbolo_actual]

    if accion > 0:  # Desplazamiento (Shift)
        pila_estados.append(accion)
        pila_simbolos.append(simbolo_actual)
        pos += 1
    elif accion < 0:  # Reducción (Reduce)
        regla = -accion - 1  # Ajuste del índice de regla
        for _ in range(lon_reglas[regla]):  # Pop según longitud de la regla
            pila_estados.pop()
            pila_simbolos.pop()
        
        estado_superior = pila_estados[-1]
        pila_estados.append(tabla[estado_superior][2])  # Empuja nuevo estado
        pila_simbolos.append(id_reglas[regla])  # Empuja símbolo reducido
    else:  # Aceptación o error
        if estado_actual == 1:
            print("Cadena aceptada")
        else:
            print("Error en el análisis")
        break

import pandas as pd
from collections import defaultdict

EPSILON = 'ε'
ENDMARKER = '$'

# Paso 1: Leer gramática desde texto
def leer_gramatica(entrada):
    gramatica = defaultdict(list)
    for linea in entrada.strip().splitlines():
        if '->' in linea:
            izquierda, derecha = linea.split('->')
            izquierda = izquierda.strip()
            producciones = [p.strip().split() for p in derecha.strip().split('|')]
            gramatica[izquierda].extend(producciones)
    return dict(gramatica)

# Paso 2: Calcular First
def calcular_first(gramatica):
    first = defaultdict(set)

    def obtener_first(simbolo):
        if simbolo not in gramatica:
            return {simbolo}
        if simbolo in first and first[simbolo]:
            return first[simbolo]
        for prod in gramatica[simbolo]:
            for simb in prod:
                first[simbolo].update(obtener_first(simb) - {EPSILON})
                if EPSILON not in obtener_first(simb):
                    break
            else:
                first[simbolo].add(EPSILON)
        return first[simbolo]

    for no_terminal in gramatica:
        obtener_first(no_terminal)
    return first

# Paso 3: Calcular Follow
def calcular_follow(gramatica, first, inicial):
    follow = defaultdict(set)
    follow[inicial].add(ENDMARKER)
    
    cambiado = True
    while cambiado:
        cambiado = False
        for A, prods in gramatica.items():
            for prod in prods:
                for i, B in enumerate(prod):
                    if B not in gramatica:
                        continue
                    siguiente = prod[i+1:]
                    primero = set()
                    for simb in siguiente:
                        simb_first = first[simb] if simb in gramatica else {simb}
                        primero.update(simb_first - {EPSILON})
                        if EPSILON not in simb_first:
                            break
                    else:
                        primero.update(follow[A])
                    if not primero.issubset(follow[B]):
                        follow[B].update(primero)
                        cambiado = True
    return follow

# Paso 4: Crear tabla LL(1)
def construir_tabla_ll1(gramatica, first, follow):
    tabla = defaultdict(lambda: defaultdict(str))
    for A, prods in gramatica.items():
        for prod in prods:
            primeros = set()
            for simb in prod:
                simb_first = first[simb] if simb in gramatica else {simb}
                primeros.update(simb_first - {EPSILON})
                if EPSILON not in simb_first:
                    break
            else:
                primeros.add(EPSILON)
            for t in primeros:
                if t != EPSILON:
                    tabla[A][t] = ' '.join(prod)
            if EPSILON in primeros:
                for f in follow[A]:
                    tabla[A][f] = EPSILON
    return tabla

# Paso 5: Exportar a CSV
def exportar_tabla_csv(tabla_ll1, terminales, archivo_salida):
    no_terminales = sorted(tabla_ll1.keys())
    data = []
    for nt in no_terminales:
        fila = [nt] + [tabla_ll1[nt].get(t, '') for t in terminales]
        data.append(fila)
    columnas = ['Non-Terminal'] + terminales
    df = pd.DataFrame(data, columns=columnas)
    df.to_csv(archivo_salida, index=False)
    print(f"Tabla LL(1) guardada en {archivo_salida}")

# Leer el archivo como UTF-8
with open("gramatica.txt", "r", encoding="utf-8") as file:
    entrada_gramatica = file.read()

# Reemplazar '' por ε
entrada_gramatica = entrada_gramatica.replace("''", EPSILON)

# Volver a escribir con codificación UTF-8
with open("gramatica.txt", "w", encoding="utf-8") as f:
    f.write(entrada_gramatica)

gramatica = leer_gramatica(entrada_gramatica)
first = calcular_first(gramatica)
follow = calcular_follow(gramatica, first, inicial='Program')
tabla_ll1 = construir_tabla_ll1(gramatica, first, follow)

# Terminales relevantes extraídos de las producciones + $
terminales = sorted(set(t for prods in gramatica.values() for p in prods for t in p if t not in gramatica and t != EPSILON))
if ENDMARKER not in terminales:
    terminales.append(ENDMARKER)

# Exportar a CSV
exportar_tabla_csv(tabla_ll1, terminales, "tabla.csv")
# Copiar al otro archivo
print(','.join(f"'{t}'" for t in sorted(terminales)))

from tabla import (
    leer_gramatica,
    calcular_first,
    calcular_follow,
    construir_tabla_ll1,
    exportar_tabla_csv,
    EPSILON,
    ENDMARKER
)

from parser import (
    procesar_tabla_analisis,
    predictive_parser,
    generar_arbol_graphviz
)

from lexer import tokenizar_frase

from semantic import (
    construir_tabla_simbolos,
    guardar_tabla, verificar_identificadores,
    verificar_redeclaraciones,
    imprimir_tabla_simbolos
)

from cgen import generar_spim, asignar_padres


import sys

def main():
    try:
        # Tokens
        with open("entrada_lex.txt", "r", encoding="utf-8") as file:
            code = file.read()
        tokens_rapidos = tokenizar_frase(code)

        # Gramatica -> Tabla
        with open("gramatica.txt", "r", encoding="utf-8") as file:
            entrada_gramatica = file.read()

        entrada_gramatica = entrada_gramatica.replace("''", EPSILON)

        with open("gramatica.txt", "w", encoding="utf-8") as f:
            f.write(entrada_gramatica)

        gramatica = leer_gramatica(entrada_gramatica)
        first = calcular_first(gramatica)
        follow = calcular_follow(gramatica, first, inicial='Program')
        tabla_ll1 = construir_tabla_ll1(gramatica, first, follow)

        # Tabla -> csv
        terminales = sorted(set(t for prods in gramatica.values() for p in prods for t in p if t not in gramatica and t != EPSILON))
        if ENDMARKER not in terminales:
            terminales.append(ENDMARKER)

        exportar_tabla_csv(tabla_ll1, terminales, "tabla.csv")

        # Parser
        procesar_tabla_analisis("tabla.csv", "producciones.csv")
        root = predictive_parser(tokens_rapidos, csv_file="producciones.csv")

        # Arbol
        generar_arbol_graphviz(root)

        # Guardar Arbol
        import pickle
        with open("arbol.pkl", "wb") as f:
            pickle.dump(root, f)

        # Semantico
        print("\n ANALIZANDO...")
        tabla = []
        construir_tabla_simbolos(root, tabla)
        guardar_tabla(tabla)
        print(f"\n Tabla de símbolos generada con {len(tabla)} símbolos.")
        imprimir_tabla_simbolos(tabla, solo_global=False)
        print("\n Verificando identificadores usados...")
        verificar_identificadores(root, tabla)
        verificar_redeclaraciones(tabla)
        imprimir_tabla_simbolos(tabla, solo_global=True)

        # SPIM
        asignar_padres(root)
        generar_spim(root)

    except Exception as e:
        print(f"\n\n -> Error fatal: {type(e).__name__}: {e}\n")
        sys.exit(1)  # Sale con código de error

if __name__ == "__main__":
    main()

#Probar SPIM
#https://shawnzhong.github.io/JsSpim/
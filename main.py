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


def main():
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
    import pickle

    # Guardar
    with open("arbol.pkl", "wb") as f:
        pickle.dump(root, f)


if __name__ == "__main__":
    main()

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

from lexer import tokenizar_frase,tokenizar_frase_sem

from semantic import (
    build_symbol_table,
    verificar_variables_usadas,
    check_duplicate_declarations,
    limpiar_tabla_simbolos,
    verificar_tipos_expresiones
)



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
    tokens_sem = tokenizar_frase_sem(code)
    tabla = build_symbol_table(tokens_sem)
    #print(tokens_sem)
    print("\nTABLA DE TODO LOS SIMBOLOS")
    for entry in tabla:
        print(f"Nombre: {entry['name']:<20}, Tipo: {entry['type']:<20}, Ámbito: {entry['scope']:<20}")

    errores = verificar_variables_usadas(tokens_sem, tabla)

    print("\nERRORES SEMÁNTICOS:")
    for e in errores:
        print(e)

    errores = check_duplicate_declarations(tabla)
    for e in errores:
        print(e)
    tabla = limpiar_tabla_simbolos(tabla,eliminar_locales=True)
    print("\nTABLA DE SIMBOLOS DEPURADA")
    for entry in tabla:
        print(f"Nombre: {entry['name']:<20}, Tipo: {entry['type']:<20}, Ámbito: {entry['scope']:<20}")

    errores_tipo = verificar_tipos_expresiones(tokens_sem, tabla)
    print("\nERRORES DE TIPO")
    for e in errores_tipo:
        print(e)
  

if __name__ == "__main__":
    main()

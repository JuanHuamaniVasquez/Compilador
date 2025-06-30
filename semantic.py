import pickle
import csv

# =======================
#  Clases y utilidades
# =======================

class Symbol:
    def __init__(self, name, tipo, scope):
        self.name = name
        self.tipo = tipo
        self.scope = scope

    def to_tuple(self):
        return (self.name, self.tipo, self.scope)

def es_tipo(nombre):
    return nombre in {"tni", "taolf", "gnirts", "naim", "loob", "diov"}

def buscar_tipo(nodo):
    """Busca un tipo válido dentro del subárbol."""
    if es_tipo(nodo.name):
        return nodo.name
    for hijo in nodo.children:
        tipo = buscar_tipo(hijo)
        if tipo:
            return tipo
    return None

def buscar_nodo(nodo, objetivo):
    """Busca el primer nodo con un nombre específico."""
    if nodo.name == objetivo:
        return nodo
    for hijo in nodo.children:
        res = buscar_nodo(hijo, objetivo)
        if res:
            return res
    return None

def buscar_id_en_E(nodo):
    """Busca recursivamente un id dentro del subárbol de E."""
    if nodo.name == "id":
        return nodo.value
    for hijo in nodo.children:
        nombre = buscar_id_en_E(hijo)
        if nombre:
            return nombre
    return None

def registrar_parametros(args_node, tabla, scope):
    if args_node is None:
        return
    #print(f" Procesando parámetros en ámbito {scope}")
    if args_node.name == "Args":
        tipo = None
        nombre = None
        for hijo in args_node.children:
            if hijo.name == "Type":
                tipo = buscar_tipo(hijo)
            elif hijo.name == "E":
                nombre = buscar_id_en_E(hijo)
        if tipo and nombre:
            #print(f" Parámetro detectado: {nombre}, tipo: {tipo}, scope: {scope}")
            tabla.append(Symbol(nombre, tipo, scope))
    for hijo in args_node.children:
        registrar_parametros(hijo, tabla, scope)

# =======================
#  Recorrido semántico
# =======================

def construir_tabla_simbolos(nodo, tabla, scope="global", visitados=None):
    if visitados is None:
        visitados = set()

    if id(nodo) in visitados:
        return  # evitar nodos duplicados
    visitados.add(id(nodo))

    #print(f" Visitando nodo: {nodo.name} (valor: {nodo.value})")

    if nodo.name == "VarDecl":
        #print(" Detectada declaración (variable o función)")
        tipo = None
        nombre = None
        es_funcion = False
        nodo_args = None
        bloque_funcion = None

        for hijo in nodo.children:
            if hijo.name == "Type":
                tipo = buscar_tipo(hijo)
                #print(f"   Tipo detectado: {tipo}")
            elif hijo.name == "E":
                f_nodo = buscar_nodo(hijo, "F")
                if f_nodo:
                    if f_nodo.children and f_nodo.children[0].name.startswith("id("):
                        nombre = f_nodo.children[0].value.split("(")[0]
                        nodo_args = buscar_nodo(f_nodo, "Args")
                        bloque_funcion = buscar_nodo(f_nodo, "Block")
                        es_funcion = True
                    else:
                        id_plano = buscar_nodo(f_nodo, "id")
                        if id_plano:
                            nombre = id_plano.value

        if tipo and nombre:
            if es_funcion:
                #print(f" Función detectada: {nombre}, tipo: {tipo}")
                tabla.append(Symbol(nombre, tipo, "global"))
                registrar_parametros(nodo_args, tabla, nombre)
                if bloque_funcion:
                    construir_tabla_simbolos(bloque_funcion, tabla, scope=nombre, visitados=visitados)
            else:
                #print(f" Variable registrada: {nombre}, tipo: {tipo}, scope: {scope}")
                tabla.append(Symbol(nombre, tipo, scope))

    for hijo in nodo.children:
        construir_tabla_simbolos(hijo, tabla, scope, visitados)

# =======================
#  Visualizador
# =======================

def imprimir_arbol(node, nivel=0):
    indent = "  " * nivel
    if node.value:
        print(f"{indent}- {node.name} ({node.value})")
    else:
        print(f"{indent}- {node.name}")
    for child in node.children:
        imprimir_arbol(child, nivel + 1)

# =======================
#  Entrada/salida
# =======================

def cargar_arbol(path="arbol.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def guardar_tabla(tabla, filename="tabla_simbolos.csv"):
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre", "tipo", "ambito"])
        for simbolo in tabla:
            writer.writerow(simbolo.to_tuple())

def verificar_identificadores(nodo, tabla, scope="global", visitados=None):
    if visitados is None:
        visitados = set()

    if id(nodo) in visitados:
        return
    visitados.add(id(nodo))

    # Si es identificador: id o id(
    if nodo.name.startswith("id"):
        nombre = nodo.value.split("(")[0] if "(" in nodo.value else nodo.value
        if not esta_en_tabla(nombre, scope, tabla):
            print(f" Error: Identificador '{nombre}' no declarado en ámbito '{scope}'")

    # Si entramos a una función, cambiar el scope
    if nodo.name == "VarDecl":
        for hijo in nodo.children:
            if hijo.name == "E":
                f_nodo = buscar_nodo(hijo, "F")
                if f_nodo and f_nodo.children and f_nodo.children[0].name.startswith("id("):
                    nuevo_scope = f_nodo.children[0].value.split("(")[0]
                    bloque = buscar_nodo(f_nodo, "Block")
                    if bloque:
                        verificar_identificadores(bloque, tabla, scope=nuevo_scope, visitados=visitados)
                    return  # no continuar para evitar doble recorrido

    # Continuar recorriendo hijos
    for hijo in nodo.children:
        verificar_identificadores(hijo, tabla, scope, visitados)

def esta_en_tabla(nombre, scope, tabla):
    # Verificar en el mismo scope
    for s in tabla:
        if s.name == nombre and s.scope == scope:
            return True
    # Verificar si existe global
    for s in tabla:
        if s.name == nombre and s.scope == "global":
            return True
    return False

def verificar_redeclaraciones(tabla):
    print("\n Verificando redeclaraciones:")
    vistos = set()
    for simbolo in tabla:
        clave = (simbolo.name, simbolo.scope)
        if clave in vistos:
            print(f" Error: '{simbolo.name}' redeclarado en ámbito '{simbolo.scope}'")
        else:
            vistos.add(clave)

def imprimir_tabla_simbolos(tabla, solo_global=False):
    from tabulate import tabulate

    # Filtrar según flag
    if solo_global:
        datos = [(s.name, s.tipo, s.scope) for s in tabla if s.scope == "global"]
    else:
        datos = [(s.name, s.tipo, s.scope) for s in tabla]

    print("\n Tabla de Símbolos:")
    print(tabulate(datos, headers=["Nombre", "Tipo", "Ámbito"], tablefmt="pretty"))

# =======================
#  INFERIR TIPOS
# =======================



# =======================
#  Main
# =======================

if __name__ == "__main__":
    raiz = cargar_arbol()
    print("\n ANALIZANDO...")
    tabla = []
    construir_tabla_simbolos(raiz, tabla)
    guardar_tabla(tabla)
    print(f"\n Tabla de símbolos generada con {len(tabla)} símbolos.")
    imprimir_tabla_simbolos(tabla, solo_global=False)
    print("\n Verificando identificadores usados...")
    verificar_identificadores(raiz, tabla)
    verificar_redeclaraciones(tabla)
    imprimir_tabla_simbolos(tabla, solo_global=True)


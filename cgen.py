# cgen.py - Generador de código SPIM para expresiones aritméticas
from semantic import cargar_arbol

contador_temporales = 0  # Global para manejar registros
temporales_usados = set()
codigo_spim = []         # Lista de strings con instrucciones generadas
variables = set()        # Para declarar en .data

def nuevo_temp():
    global contador_temporales
    temp = f"$t{contador_temporales}"
    temporales_usados.add(temp)
    contador_temporales = (contador_temporales + 1) % 10
    return temp

def buscar_nodo(nodo, nombre):
    if nodo.name == nombre:
        return nodo
    for hijo in nodo.children:
        resultado = buscar_nodo(hijo, nombre)
        if resultado:
            return resultado
    return None

def generar_codigo_expresion(nodo, izq=None):

    if nodo is None:
        return ""

    if len(nodo.children) == 0:
        if nodo.name == "num":
            temp = nuevo_temp()
            codigo_spim.append(f"# Cargar constante {nodo.value}")
            codigo_spim.append(f"li {temp}, {nodo.value}")
            return temp
        elif nodo.name == "id":
            variables.add(nodo.value)
            temp = nuevo_temp()
            codigo_spim.append(f"# Cargar valor de variable {nodo.value}")
            codigo_spim.append(f"lw {temp}, {nodo.value}")
            return temp
        elif nodo.name == "eurt":
            temp = nuevo_temp()
            codigo_spim.append(f"# Cargar valor constante 1")
            codigo_spim.append(f"li {temp}, 1")
            return temp
        elif nodo.name == "eslaf":
            temp = nuevo_temp()
            codigo_spim.append(f"# Cargar valor constante 0")
            codigo_spim.append(f"li {temp}, 0")
            return temp
        else:
            return ""

    if nodo.name == "F":
        return generar_codigo_expresion(nodo.children[0])

    if nodo.name == "G":
        f = generar_codigo_expresion(nodo.children[0])
        gprima = nodo.children[1] if len(nodo.children) > 1 else None
        if gprima and len(gprima.children) >= 2 and gprima.children[0].value == "=":
            expr = generar_codigo_expresion(gprima.children[1])
            return expr
        return f

    if nodo.name == "T'":
        if len(nodo.children) == 0:
            return izq  # Nada que hacer

        op = nodo.children[0].value
        derecho = generar_codigo_expresion(nodo.children[1])
        siguiente = generar_codigo_expresion(nodo.children[2]) if len(nodo.children) > 2 else None

        temp = nuevo_temp()
        if op == "*":
            codigo_spim.append(f"# Operación * entre {izq} y {derecho}")
            codigo_spim.append(f"mul {temp}, {izq}, {derecho}")
        elif op == "/":
            codigo_spim.append(f"# Operación / entre {izq} y {derecho}")
            codigo_spim.append(f"div {izq}, {derecho}")
            codigo_spim.append(f"mflo {temp}")
        if siguiente:
            return generar_codigo_expresion_recursiva(temp, nodo.children[2])
        return temp

    if nodo.name == "T":
        izq = generar_codigo_expresion(nodo.children[0])
        der = generar_codigo_expresion_recursiva(izq, nodo.children[1]) if len(nodo.children) > 1 else izq
        return der 
    
    if nodo.name == "E'":
        if len(nodo.children) == 0:
            return izq  # Nada que hacer

        op = nodo.children[0].value
        derecho = generar_codigo_expresion(nodo.children[1])
        siguiente = generar_codigo_expresion(nodo.children[2]) if len(nodo.children) > 2 else None

        temp = nuevo_temp()
        if op == "+" :
            codigo_spim.append(f"# Operación + entre {izq} y {derecho}")
            codigo_spim.append(f"add {temp}, {izq}, {derecho}")
        elif op == "-" and izq:
            codigo_spim.append(f"# Operación - entre {izq} y {derecho}")
            codigo_spim.append(f"sub {temp}, {izq}, {derecho}")
        if siguiente:
            return generar_codigo_expresion_recursiva(temp, nodo.children[2])
        return temp


    if nodo.name == "E":
        izq = generar_codigo_expresion(nodo.children[0])
        der = generar_codigo_expresion_recursiva(izq, nodo.children[1]) if len(nodo.children) > 1 else izq
        return der 
    return ""

def generar_codigo_completo(nodo):
    if nodo.name == "VarDecl":
        g_nodo = buscar_nodo(nodo, "G")
        if g_nodo:
            id_nodo = buscar_nodo(g_nodo, "id")
            if id_nodo:
                nombre = id_nodo.value
                variables.add(nombre)

                e_nodo = buscar_nodo(nodo, "E")
                if e_nodo:
                    eprima = e_nodo.children[1] if len(e_nodo.children) > 1 else None
                    if eprima and len(eprima.children) >= 3:
                        print(f"[DEBUG] Generando código completo para expresión de '{nombre}'")
                        resultado = generar_codigo_expresion(e_nodo)
                        if resultado:
                            codigo_spim.append(f"# Guardar resultado en variable {nombre}")
                            codigo_spim.append(f"sw {resultado}, {nombre}")
                    else:
                        gprima = g_nodo.children[1] if len(g_nodo.children) > 1 else None
                        if gprima and len(gprima.children) >= 2 and gprima.children[0].value == "=":
                            valor_nodo = gprima.children[1]
                            if valor_nodo.name == "F" and valor_nodo.children[0].name == "num":
                                num = valor_nodo.children[0].value
                                temp = nuevo_temp()
                                codigo_spim.append(f"# Cargar constante {num}")
                                codigo_spim.append(f"li {temp}, {num}")
                                codigo_spim.append(f"# Asignar valor directo a '{nombre}'")
                                codigo_spim.append(f"sw {temp}, {nombre}")

    for hijo in nodo.children:
        generar_codigo_completo(hijo)

def generar_spim(nodo_raiz, archivo_salida="salida.asm"):
    global codigo_spim, contador_temporales, variables, temporales_usados
    codigo_spim = []
    contador_temporales = 0
    variables = set()
    temporales_usados = set()

    generar_codigo_completo(nodo_raiz)

    data = ".data\n" + "\n".join([f"{var}: .word 0" for var in sorted(variables)])
    cuerpo = ["    " + instr for instr in codigo_spim]

    # Agregar impresión de valores de todas las variables
    for var in sorted([v for v in variables if isinstance(v, str)]):
        cuerpo.append(f'    # Imprimir variable {var}')
        cuerpo.append(f'    li $v0, 4')
        cuerpo.append(f'    la $a0, msg_{var}')
        cuerpo.append('    syscall')
        cuerpo.append(f'    lw $a0, {var}')
        cuerpo.append(f'    li $v0, 1')
        cuerpo.append('    syscall')
        cuerpo.append(f'    li $v0, 4')
        cuerpo.append(f'    la $a0, newline')
        cuerpo.append('    syscall')

    cuerpo.append("    li $v0, 10")
    cuerpo.append("    syscall")

    # Mensajes auxiliares
    mensajes = [f'{label}: .asciiz "{contenido}"' for v in variables if isinstance(v, tuple) for (label, contenido) in [v]]
    mensajes += [f'msg_{var}: .asciiz "{var} = "' for var in sorted(variables) if isinstance(var, str)]
    mensajes.append('newline: .asciiz "\\n"')

    vars_normales = [f'{var}: .word 0' for var in sorted(variables) if isinstance(var, str)]
    data = ".data\n" + "\n".join(vars_normales + mensajes)
    text = ".text\nmain:\n" + "\n".join(cuerpo)


    codigo_final = data + "\n\n" + text

    # Eliminar líneas que contienen "None"
    lineas = codigo_final.splitlines()
    lineas_limpias = [linea for linea in lineas if "None" not in linea]
    codigo_limpio = "\n".join(lineas_limpias)

    with open(archivo_salida, "w") as f:
        f.write(codigo_limpio)


    print(f"\nCódigo SPIM guardado en '{archivo_salida}'")  
def asignar_padres(nodo, padre=None):
    nodo.parent = padre
    for hijo in nodo.children:
        asignar_padres(hijo, nodo)
def generar_codigo_expresion_recursiva(izq, nodo):
    if nodo is None or len(nodo.children) == 0:
        return izq

    op = nodo.children[0].value
    derecho = generar_codigo_expresion(nodo.children[1])
    siguiente = nodo.children[2] if len(nodo.children) > 2 else None

    temp = nuevo_temp()
    if nodo.name == "T'":  # multiplicación/división
        if op == "*":
            codigo_spim.append(f"# Operación * entre {izq} y {derecho}")
            codigo_spim.append(f"mul {temp}, {izq}, {derecho}")
        elif op == "/":
            codigo_spim.append(f"# Operación / entre {izq} y {derecho}")
            codigo_spim.append(f"div {izq}, {derecho}")
            codigo_spim.append(f"mflo {temp}")
    elif nodo.name == "E'":  # suma/resta
        if op == "+":
            codigo_spim.append(f"# Operación + entre {izq} y {derecho}")
            codigo_spim.append(f"add {temp}, {izq}, {derecho}")
        elif op == "-":
            codigo_spim.append(f"# Operación - entre {izq} y {derecho}")
            codigo_spim.append(f"sub {temp}, {izq}, {derecho}")
    else:
        # Nodo inesperado, retornar acumulado sin cambios
        return izq

    if siguiente:
        return generar_codigo_expresion_recursiva(temp, siguiente)
    else:
        return temp


'''if __name__ == "__main__":
    raiz = cargar_arbol()
    asignar_padres(raiz)
    generar_spim(raiz)'''
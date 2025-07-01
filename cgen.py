# cgen.py - Generador de código SPIM para expresiones aritméticas
from semantic import cargar_arbol # Keep this, but handle its potential failure

contador_temporales = 0  # Global para manejar registros
temporales_usados = set()
codigo_spim = []         # Lista de strings con instrucciones generadas
variables = set()        # Para declarar en .data

def nuevo_temp():
    global contador_temporales
    temp = f"$t{contador_temporales}"
    temporales_usados.add(temp)
    contador_temporales = (contador_temporales + 1) % 10 # Cycle through t0-t9
    return temp

def buscar_nodo(nodo, nombre): # This helper might not be needed with direct AST traversal
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

    if len(nodo.children) == 0:  # Terminal nodes
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
            codigo_spim.append(f"# Cargar booleano true (1)")
            codigo_spim.append(f"li {temp}, 1")
            return temp
        elif nodo.name == "eslaf":
            temp = nuevo_temp()
            codigo_spim.append(f"# Cargar booleano false (0)")
            codigo_spim.append(f"li {temp}, 0")
            return temp
        else:
            return ""

    if nodo.name == "F":
        if len(nodo.children) == 1: # Handles F -> (E), F -> id, F -> num, F -> eurt, F -> eslaf
             return generar_codigo_expresion(nodo.children[0])
        return ""

    if nodo.name == "G'":
        if len(nodo.children) == 0:
            return izq

        op_node = nodo.children[0]
        op = op_node.value

        f_operand_node = nodo.children[1]
        derecho = generar_codigo_expresion(f_operand_node)

        temp = nuevo_temp()
        print(f"[DEBUG G'] op: '{op}', izq: '{izq}', derecho: '{derecho}', temp_for_result: '{temp}'") # DEBUG PRINT
        codigo_spim.append(f"# Operación {op} entre {izq} y {derecho}")

        if op == "==":
            codigo_spim.append(f"seq {temp}, {izq}, {derecho}")
        elif op == "!=":
            codigo_spim.append(f"sne {temp}, {izq}, {derecho}")
        elif op == "<":
            codigo_spim.append(f"slt {temp}, {izq}, {derecho}")
        elif op == "<=":
            temp_aux = nuevo_temp()
            codigo_spim.append(f"sgt {temp_aux}, {izq}, {derecho}")
            codigo_spim.append(f"xori {temp}, {temp_aux}, 1")
        elif op == ">":
            codigo_spim.append(f"sgt {temp}, {izq}, {derecho}")
        elif op == ">=":
            temp_aux = nuevo_temp()
            codigo_spim.append(f"slt {temp_aux}, {izq}, {derecho}")
            codigo_spim.append(f"xori {temp}, {temp_aux}, 1")
        elif op == "&&":
            codigo_spim.append(f"and {temp}, {izq}, {derecho}")
        elif op == "%":
            codigo_spim.append(f"div {izq}, {derecho}")
            codigo_spim.append(f"mfhi {temp}")

        if len(nodo.children) > 2:
            return generar_codigo_expresion(nodo.children[2], temp)
        return temp

    if nodo.name == "G":
        val_f = generar_codigo_expresion(nodo.children[0])
        if len(nodo.children) > 1:
            return generar_codigo_expresion(nodo.children[1], val_f)
        return val_f

    if nodo.name == "T'":
        if len(nodo.children) == 0:
            return izq

        op = nodo.children[0].value
        derecho = generar_codigo_expresion(nodo.children[1])

        temp = nuevo_temp()
        codigo_spim.append(f"# Operación {op} entre {izq} y {derecho}")
        if op == "*":
            codigo_spim.append(f"mul {temp}, {izq}, {derecho}")
        elif op == "/":
            codigo_spim.append(f"div {izq}, {derecho}")
            codigo_spim.append(f"mflo {temp}")

        if len(nodo.children) > 2:
            return generar_codigo_expresion(nodo.children[2], temp)
        return temp

    if nodo.name == "T":
        val_g = generar_codigo_expresion(nodo.children[0])
        if len(nodo.children) > 1:
            return generar_codigo_expresion(nodo.children[1], val_g)
        return val_g

    if nodo.name == "E'":
        if len(nodo.children) == 0:
            return izq

        op = nodo.children[0].value
        derecho = generar_codigo_expresion(nodo.children[1]) # This is a T node

        temp = nuevo_temp()
        codigo_spim.append(f"# Operación {op} entre {izq} y {derecho}")
        if op == "+":
            codigo_spim.append(f"add {temp}, {izq}, {derecho}")
        elif op == "-" and izq:
            codigo_spim.append(f"sub {temp}, {izq}, {derecho}")

        if len(nodo.children) > 2: # Next E' node
             return generar_codigo_expresion(nodo.children[2], temp)
        return temp

    if nodo.name == "E":
        val_t = generar_codigo_expresion(nodo.children[0])
        if len(nodo.children) > 1:
            return generar_codigo_expresion(nodo.children[1], val_t)
        return val_t

    return ""

def generar_codigo_completo(nodo):
    if nodo.name == "VarDecl":
        # Grammar: VarDecl -> Type E
        # E will be structured for assignment like: id = expression_value
        # E -> T -> G -> F(id) G' -> = F(expression_value) G'(epsilon)

        type_node = nodo.children[0] # Not used in cgen, but part of grammar
        e_node_for_assignment = nodo.children[1]

        id_node_val = None
        expr_node_for_value = None

        # Traverse E to find the 'id' and the expression part of 'id = expr'
        # E -> T -> G -> F (id) G' (-> = F(value_expr) G'(eps))
        if e_node_for_assignment.name == "E" and len(e_node_for_assignment.children) > 0:
            t_node = e_node_for_assignment.children[0]
            if t_node.name == "T" and len(t_node.children) > 0:
                g_node = t_node.children[0]
                if g_node.name == "G" and len(g_node.children) == 2: # Expect F and G'
                    f_node_for_id = g_node.children[0]
                    g_prime_node_for_eq = g_node.children[1]

                    if (f_node_for_id.name == "F" and len(f_node_for_id.children) == 1 and
                        f_node_for_id.children[0].name == "id"):
                        id_node_val = f_node_for_id.children[0].value
                        variables.add(id_node_val)

                        if (g_prime_node_for_eq.name == "G'" and len(g_prime_node_for_eq.children) >=2 and
                            g_prime_node_for_eq.children[0].value == "="):
                            expr_node_for_value = g_prime_node_for_eq.children[1] # This is an F node

        if id_node_val and expr_node_for_value:
            codigo_spim.append(f"# Initialization for variable {id_node_val}")
            resultado_expr = generar_codigo_expresion(expr_node_for_value)
            if resultado_expr:
                codigo_spim.append(f"sw {resultado_expr}, {id_node_val}")
        elif id_node_val: # Declaration without assignment in this structure (e.g. tni x;)
             variables.add(id_node_val) # Ensure it's declared
             codigo_spim.append(f"# Declaration for variable {id_node_val} (default 0)")


    elif nodo.name not in ["Program", "Stmt"]: # Avoid re-processing children if not needed
        # This is a generic traversal; specific statements like IfStmt, WhileStmt would need handlers
        # For simple expressions or VarDecl, this might not be hit if handled above.
        # If we have an ExprStmt -> E, then E needs to be evaluated.
        # Let's assume for now 'generar_codigo_completo' is called on 'Program' or 'Stmt' list.
        pass # Placeholder for other statement processing logic

    # General traversal for program structure (e.g., Program -> Stmt Program)
    if nodo.name in ["Program", "Block", "Stmt"]: # Nodes that contain sequences of statements/other structures
        for hijo in nodo.children:
            generar_codigo_completo(hijo)


def generar_spim(nodo_raiz, archivo_salida="salida.asm"):
    global codigo_spim, contador_temporales, variables, temporales_usados
    codigo_spim = []
    contador_temporales = 0
    variables = set()
    temporales_usados = set()

    generar_codigo_completo(nodo_raiz)

    data_section = [".data"]
    for var in sorted(list(variables)):
        data_section.append(f"{var}: .word 0")

    text_section = [".text", ".globl main", "main:"] # Added .globl main
    text_section.extend(["    " + instr for instr in codigo_spim])

    text_section.append("    # Exit program")
    text_section.append("    li $v0, 10")
    text_section.append("    syscall")

    codigo_final = "\n".join(data_section) + "\n\n" + "\n".join(text_section)

    with open(archivo_salida, "w") as f:
        f.write(codigo_final)

    print(f"\nCódigo SPIM guardado en '{archivo_salida}'")  

# Removed asignar_padres and generar_codigo_expresion_recursiva as they are not used with the new structure.

if __name__ == "__main__":
    class DummyNode:
        def __init__(self, name, value=None, children=None):
            self.name = name
            self.value = value
            self.children = children if children else []
            # self.parent = None # Not used by cgen logic directly

    # AST for: tni result = (5 > 3) && (1 < 2);
    F_5 = DummyNode("F", children=[DummyNode("num", value=5)])
    F_3 = DummyNode("F", children=[DummyNode("num", value=3)])
    Gp_gt = DummyNode("G'", children=[DummyNode(">", value=">"), F_3, DummyNode("G'")]) # G' -> > F G'(eps)
    G_5gt3 = DummyNode("G", children=[F_5, Gp_gt]) # G -> F G'
    T_5gt3 = DummyNode("T", children=[G_5gt3, DummyNode("T'")]) # T -> G T'(eps)
    E_5gt3 = DummyNode("E", children=[T_5gt3, DummyNode("E'")]) # E -> T E'(eps)
    F_5gt3_expr = DummyNode("F", children=[E_5gt3]) # F -> (E)

    F_1 = DummyNode("F", children=[DummyNode("num", value=1)])
    F_2 = DummyNode("F", children=[DummyNode("num", value=2)])
    Gp_lt = DummyNode("G'", children=[DummyNode("<", value="<"), F_2, DummyNode("G'")])
    G_1lt2 = DummyNode("G", children=[F_1, Gp_lt])
    T_1lt2 = DummyNode("T", children=[G_1lt2, DummyNode("T'")])
    E_1lt2 = DummyNode("E", children=[T_1lt2, DummyNode("E'")])
    F_1lt2_expr = DummyNode("F", children=[E_1lt2]) # F -> (E)

    # Building ( (5>3) && (1<2) )
    # G_main_and will have F_5gt3_expr as its F child, and G'_and_op as its G' child
    # G'_and_op will have '&&' as op, F_1lt2_expr as its F child
    Gp_and = DummyNode("G'", children=[DummyNode("&&", value="&&"), F_1lt2_expr, DummyNode("G'")]) # G' -> && F G'(eps)
    G_and_expr = DummyNode("G", children=[F_5gt3_expr, Gp_and]) # G -> F G' (where F is (5>3))
    T_and_expr = DummyNode("T", children=[G_and_expr, DummyNode("T'")])
    E_and_expr = DummyNode("E", children=[T_and_expr, DummyNode("E'")])
    F_final_expr_val = DummyNode("F", children=[E_and_expr]) # This F node wraps the whole boolean expression

    # For assignment: result = F_final_expr_val
    F_id_result = DummyNode("F", children=[DummyNode("id", value="result")])
    # G' for assignment: G' -> = F G'(eps)
    Gp_assign = DummyNode("G'", children=[DummyNode("=", value="="), F_final_expr_val, DummyNode("G'")])
    # G for assignment: G -> F(id) G'(assign)
    G_assign = DummyNode("G", children=[F_id_result, Gp_assign])
    T__assign_stmt = DummyNode("T", children=[G_assign, DummyNode("T'")]) # T -> G T'(eps)
    E_assign_stmt = DummyNode("E", children=[T__assign_stmt, DummyNode("E'")]) # E -> T E'(eps) # Corrected variable name

    # VarDecl node: VarDecl -> Type E(assign_stmt)
    VarDecl_node = DummyNode("VarDecl", children=[DummyNode("Type", value="tni"), E_assign_stmt]) # Type can be anything
    Stmt_node = DummyNode("Stmt", children=[VarDecl_node])
    raiz_dummy = DummyNode("Program", children=[Stmt_node]) # Program -> Stmt

    try:
        # Attempt to load the real AST first
        raiz = cargar_arbol()
        if raiz:
            # If semantic tree is loaded, use it (and it needs 'asignar_padres' if semantic.py doesn't do it)
            # For now, assuming cgen doesn't need parent pointers for its logic.
            # asignar_padres(raiz)
            print("Árbol semántico cargado desde arbol.pkl. Generando SPIM...")
            generar_spim(raiz)
        else:
            # This case implies cargar_arbol returned None, not an exception (e.g. file empty or invalid format but not missing)
            print("No se pudo cargar el árbol semántico (arbol.pkl) o es None. Usando árbol de prueba dummy.")
            generar_spim(raiz_dummy, "salida_dummy.asm")
    except FileNotFoundError:
        print("!!! CAUGHT FileNotFoundError: arbol.pkl no encontrado. Usando árbol de prueba dummy. !!!")
        generar_spim(raiz_dummy, "salida_dummy.asm")
    except Exception as e:
        # Catch any other errors during cargar_arbol or initial processing
        print(f"Ocurrió un error general al intentar cargar arbol.pkl: {e}")
        print("Usando árbol de prueba dummy.")
        # import traceback # Uncomment for more detailed debugging if this path is hit unexpectedly
        # traceback.print_exc() # Uncomment for more detailed debugging
        generar_spim(raiz_dummy, "salida_dummy.asm")

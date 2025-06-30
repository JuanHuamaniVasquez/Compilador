import pandas as pd

class TreeNode:
    def __init__(self, name, value=None):
        self.name = name  # Símbolo gramatical
        self.value = value  # Valor del token (solo para terminales)
        self.children = []

    def __str__(self):
        return f"{self.name}:{self.value}" if self.value else self.name


def read_parsing_table(csv_file):
    df = pd.read_csv(csv_file)
    parsing_table = {}
    for _, row in df.iterrows():
        non_terminal = row['NonTerminal']
        terminal = row['Terminal']
        production = row['Production']
        if non_terminal not in parsing_table:
            parsing_table[non_terminal] = {}
        production_list = [] if pd.isna(production) or production.strip() == "" else production.split()
        parsing_table[non_terminal][terminal] = production_list
    return parsing_table

def predictive_parser(input_tokens, csv_file="producciones.csv"):
    parsing_table = read_parsing_table(csv_file)
    stack = [(TreeNode('$'), '$'), (TreeNode('Program'), 'Program')]
    
    # Agregamos símbolo fin de entrada
    input_tokens = input_tokens.copy()
    input_tokens.append(('$', '$'))  # ahora es una tupla

    pointer = 0
    root = stack[-1][0]  # Raíz del árbol

    print(f"{'Pila':<80} {'Entrada':<80} {'Acción'}")
    print("-" * 150)

    while stack:
        print(f"{' '.join(s for _, s in stack[::-1]):<80} {' '.join(tok[0] for tok in input_tokens[pointer:]):<80}", end=" ")
        top_node, top = stack.pop()
        current_token_type, current_token_value = input_tokens[pointer]

        if top == current_token_type == '$':
            print("ACEPTAR")
            break
        elif top in ['!=','"','$','%','&&','(',')','*','+','+=',',','-','-=','/',';','<','<=','=','==','>','>=',
                     'diov','elihw','eslaf','esle','eurt','fed','fi','id','id(','nruter','num','od','rof(','taolf',
                     'tni','tnirp(','{','}','loob','gnirts','string']:
            if top == current_token_type:
                top_node.value = current_token_value  #  Guardar el valor del token
                print("terminal")
                pointer += 1
            else:
                print("ERROR: desajuste de terminal")
                break
        elif top in parsing_table:
            rule = parsing_table[top].get(current_token_type)
            if rule is not None:
                print(f"{' '.join(rule) if rule else 'ε'}")
                # Crear nodos hijos y agregarlos
                children_nodes = [TreeNode(symbol) for symbol in rule]
                top_node.children.extend(children_nodes)
                for child_node, symbol in zip(reversed(children_nodes), reversed(rule)):
                    stack.append((child_node, symbol))
            else:
                print("ERROR: no se encontró regla")
                break
        else:
            print(f"ERROR: símbolo desconocido {top}")
            break

    return root

def procesar_tabla_analisis(archivo_entrada, archivo_salida):
    df = pd.read_csv(archivo_entrada)
    terminales = df.columns[1:].tolist()
    producciones = []
    for _, fila in df.iterrows():
        no_terminal = fila['Non-Terminal']
        for terminal in terminales:
            produccion = fila[terminal]
            if pd.isna(produccion) or produccion == '':
                continue
            if produccion == 'ε':
                produccion = ''
            producciones.append({
                'NonTerminal': no_terminal,
                'Terminal': terminal,
                'Production': produccion
            })
    df_salida = pd.DataFrame(producciones)
    df_salida.to_csv(archivo_salida, index=False)
    print(f"Archivo generado exitosamente: {archivo_salida}")

def generar_arbol_graphviz(node, filename="arbol_sintactico"):
    node_counter = 0
    dot_lines = ["digraph G {", "  node [fontname=Arial];"]

    # Lista de terminales
    terminales = {'!=','"','$','%','&&','(',')','*','+','+=',',','-','-=','/',';','<','<=','=','==','>','>=','string','diov','gnirts','elihw','eslaf','loob','esle','eurt','fed','fi','id','id(','nruter','num','od','rof(','taolf','tni','tnirp(','{','}'}

    def build_graph(node, parent_id=None):
        nonlocal node_counter
        current_id = node_counter
        node_counter += 1

        # Estilo según si es terminal o no
        if node.name in terminales:
            dot_lines.append(f'  node{current_id} [label="{node.value}", style=filled, fillcolor=lightblue, shape=box];')
        else:
            dot_lines.append(f'  node{current_id} [label="{node.name}"];')

        # Conexión con el padre
        if parent_id is not None:
            dot_lines.append(f'  node{parent_id} -> node{current_id};')

        # Procesar hijos
        for child in node.children:
            build_graph(child, current_id)

    build_graph(node)
    dot_lines.append("}")

    # Escribir archivo .dot
    dot_filename = f"{filename}.dot"
    with open(dot_filename, "w") as f:
        f.write("\n".join(dot_lines))

    print(f"Archivo DOT generado: {dot_filename}")



if __name__ == "__main__":
    archivo_entrada = 'tabla.csv'
    archivo_salida = 'producciones.csv'
    procesar_tabla_analisis(archivo_entrada, archivo_salida)
    #PRINT
    input_string = ['tni', 'id(', ')', '{', 'tnirp(', 'id', ')', 'nruter', 'num', '}']
    #BUCLES ANIDADOS
    #input_string = ['tni', 'id(', ')', '{', 'tni', 'id', '=', 'num', 'elihw', '(', 'id', '<', 'num', ')', '{', 'tni', 'id', '=', 'num', 'elihw', '(', 'id', '<', 'num', ')', '{', 'id(', 'id', ',', 'id', ',', 'id', ')', 'id', '=', 'id', '+', 'num', '}', 'id', '=', 'id', '+', 'num', '}', 'nruter', 'num', '}']
    #RECURSIVIDAD
    #input_string = ['diov', 'id(', 'tni', 'id', ')', '{', 'fi', '(', 'id', '==', 'num', ')', '{', 'nruter', 'num', '}', 'nruter', 'id', '*', 'id(', 'id', '-', 'num', ')', '}', 'tni', 'id(', ')', '{', 'tni', 'id', '=', 'id(', 'num', ')', 'id(', 'id', ')', 'nruter', 'num', '}']
    root = predictive_parser(input_string, csv_file=archivo_salida)
    generar_arbol_graphviz(root)
    

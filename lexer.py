import ply.lex as lex
import re

# Lista de nombres de los tokens (según tu tabla de tokens)
tokens = [
    'ID', 'INTEGER', 'FLOATING',
    'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'INCREMENT', 'DECREMENT', 'EQUAL', 'NOT_EQUAL',
    'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL',
    'LOGICAL_AND', 'LOGICAL_OR', 'LOGICAL_NOT',
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIV_ASSIGN',
    'TERNARY_Q', 'TERNARY_C', 'MEMBER_ACCESS', 'POINTER_ACCESS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'STRING', 'CHARACTER'
]

# Palabras reservadas (reversed)
reserved = {
    'gnirts': 'type_string',
    'tni': 'type_int',
    'tnirp': 'PRINT',
    'taolf': 'type_float',
    'elbuod': 'type_double',
    'rahc': 'type_char',
    'loob': 'type_bool',
    'diov': 'type_void',
    'trohs': 'type_short',
    'gnol': 'type_long',
    'dengisnu': 'type_unsigned',
    'gnolgnol': 'type_longlong',
    'dengis': 'type_signed',
    't_rahcw': 'type_wchar_t',
    'fi': 'IF',
    'esle': 'ELSE',
    'rof': 'FOR',
    'elihw': 'WHILE',
    'od': 'DO',
    'nruter': 'RETURN',
    'kaerb': 'BREAK',
    'eunitnoc': 'CONTINUE',
    'hctiws': 'SWITCH',
    'esac': 'CASE',
    'tluafed': 'DEFAULT',
    'ssalc': 'CLASS',
    'tcurts': 'STRUCT',
    'cilbup': 'PUBLIC',
    'etavirp': 'PRIVATE',
    'detcetorp': 'PROTECTED',
    'tsnoc': 'CONST',
    'citats': 'STATIC',
    'wen': 'NEW',
    'eteled': 'DELETE'
}

# Añadimos las palabras reservadas a la lista de tokens
tokens += list(reserved.values())

# Expresiones regulares de operadores y delimitadores
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_LOGICAL_AND = r'&&'
t_LOGICAL_OR = r'\|\|'
t_LOGICAL_NOT = r'!'
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_TERNARY_Q = r'\?'
t_TERNARY_C = r':'
t_MEMBER_ACCESS = r'\.'
t_POINTER_ACCESS = r'->'

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','

# Literales de cadenas y caracteres
t_STRING = r'\".*?\"'
t_CHARACTER = r'\'.\''

# Reglas con acciones

def t_FLOATING(t):
    r'\d+\.\d+([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es palabra reservada
    return t
# Ignorar comentarios de una sola línea (// comentario)
def t_COMMENT(t):
    r'//.*'
    pass  # No se devuelve ningún token, simplemente se ignora
# Comentarios de bloque: /* ... */
def t_COMMENT_BLOCK(t):
    r'/\*[\s\S]*?\*/'
    pass  # Ignorar token
# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Leer archivo de entrada
with open("entrada_lex.txt", "r") as file:
    code = file.read()

# Analizar el contenido
lexer.input(code)

# Mostrar tokens
print("Tokens encontrados:\n")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{tok.type:<15} {tok.value:<20} (linea {tok.lineno})")

def tokenizar_frase(frase):
    # Reemplazar '' por ε
    frase = frase.replace("''", 'ε')

    # Eliminar comentarios multilínea /* ... */
    frase = re.sub(r'/\*.*?\*/', '', frase, flags=re.DOTALL)

    # Eliminar comentarios de línea //
    frase = re.sub(r'//.*', '', frase)

    patron = r"""
        \"[^"\n]*\"         |   # strings dobles
        \'[^'\n]*\'         |   # caracteres o strings simples
        \+\+|--             |   # incrementos / decrementos
        ==|!=|<=|>=         |   # comparaciones dobles
        \+=|-=|\*=|/=       |   # asignaciones compuestas
        &&|\|\|             |   # operadores lógicos dobles
        \d+\.\d+            |   #  flotantes (antes del punto suelto)
        \d+                 |   # enteros
        \w+\(               |   # nombre de función + paréntesis
        ->|\.               |   # acceso a puntero o miembro
        [\(\){}\[\];,:]     |   # símbolos especiales
        [<>!=+\-*/%]        |   # operadores simples
        \w+                 |   # palabras
        ε                   |   # epsilon
        .                       # cualquier otro carácter
    """
    tokens = re.findall(patron, frase, flags=re.VERBOSE)

    resultado = []
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok == 'ε':
            resultado.append(('ε', 'ε'))
        elif tok.startswith('eurt') or tok.startswith("eslaf"):
            resultado.append((tok, tok)) 
        elif tok.startswith('"') or tok.startswith("'"):
            resultado.append(('id', tok))  # o puedes usar otro tipo: string o char
        elif tok.endswith('(') and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\($', tok):
            nombre_funcion = tok[:-1]
            if nombre_funcion in reserved:
                resultado.append((nombre_funcion + '(', tok))
            else:
                resultado.append(('id(', tok))
        elif re.match(r'^\d+\.\d+$', tok):  
            resultado.append(('num', tok))  # sigue siendo 'num', pero con . lo interpretamos como float más adelante
        elif tok.isdigit():
            resultado.append(('num', tok))
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tok):
            if tok in reserved:
                resultado.append((tok, tok))
            else:
                resultado.append(('id', tok))
        else:
            resultado.append((tok, tok))

    return resultado

'''print("\nTokens por tokenizar_frase:")
tokens_rapidos = tokenizar_frase(code)
print(tokens_rapidos)'''


import re

def tokenizar_frase_sem(frase):
    frase = frase.replace("''", 'ε')
    frase = re.sub(r'/\*.*?\*/', '', frase, flags=re.DOTALL)  # comentarios /* ... */
    frase = re.sub(r'//.*', '', frase)  # comentarios //

    patron = r"""
        \"[^"\n]*\"         |   # strings dobles
        \'[^'\n]*\'         |   # caracteres o strings simples
        \+\+|--             |   # incrementos / decrementos
        ==|!=|<=|>=         |   # comparaciones dobles
        \+=|-=|\*=|/=       |   # asignaciones compuestas
        &&|\|\|             |   # operadores lógicos dobles
        \d+\.\d+            |   #  flotantes (antes del punto suelto)
        \d+                 |   # enteros
        \w+\(               |   # nombre de función + paréntesis
        ->|\.               |   # acceso a puntero o miembro
        [\(\){}\[\];,:]     |   # símbolos especiales
        [<>!=+\-*/%]        |   # operadores simples
        \w+                 |   # palabras
        ε                   |   # epsilon
        .                       # cualquier otro carácter
    """

    tokens = re.findall(patron, frase, flags=re.VERBOSE)

    resultado = []
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok == 'ε':
            resultado.append(('ε', 'ε'))
        elif tok in ['eurt', 'eslaf']:
            resultado.append((tok, tok))
        elif tok.startswith('"') or tok.startswith("'"):
            resultado.append(('string', tok))
        elif tok.endswith('(') and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\($', tok):
            nombre_funcion = tok[:-1]
            if nombre_funcion in reserved:
                resultado.append((nombre_funcion, nombre_funcion))
                resultado.append(('(', '('))
            else:
                resultado.append(('id', nombre_funcion))
                resultado.append(('(', '('))
        elif re.match(r'^\d+\.\d+$', tok):  
            resultado.append(('num', tok))  # float
        elif tok.isdigit():
            resultado.append(('num', tok))  # int
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tok):
            if tok in reserved:
                resultado.append((tok, tok))
            else:
                resultado.append(('id', tok))
        else:
            resultado.append((tok, tok))

    return resultado

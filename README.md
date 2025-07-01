# Proyecto Final - Compilador

Este proyecto es el resultado final para el curso de Compiladores. Consiste en el desarrollo de un compilador que traduce un lenguaje de programación propio a código ensamblador SPIM.

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Especificación Léxica](#especificación-léxica)
3. [Gramática](#gramática)
4. [Implementación](#implementación)
    1. [Entrada](#entrada)
    2. [Salida](#salida)
    3. [Fases del Compilador](#fases-del-compilador)
        1. [Analizador Léxico](#analizador-léxico)
        2. [Analizador Sintáctico](#analizador-sintáctico)
        3. [Analizador Semántico](#analizador-semántico)
        4. [Generación de Código](#generación-de-código)
    4. [Manejo de Errores](#manejo-de-errores)
    5. [Enlace al Repositorio](#enlace-al-repositorio)
5. [Conclusiones](#conclusiones)
6. [Estructura del Repositorio](#estructura-del-repositorio)
7. [Cómo Ejecutar](#cómo-ejecutar)

## Introducción
En el vasto mundo de la programación, dar los primeros pasos puede ser un desafío. La barrera del idioma y la abstracción de los comandos suelen ser obstáculos comunes para los nuevos aprendices. SKRN nace de la necesidad de simplificar este proceso inicial, buscando tender un puente entre el lenguaje natural y los conceptos de programación. La idea central es desmitificar la sintaxis y permitir que los estudiantes se concentren en la lógica y los fundamentos, fomentando una comprensión más intuitiva y una curva de aprendizaje más suave.

SKRN es un lenguaje de programación interpretado, diseñado específicamente para facilitar el aprendizaje de los conceptos fundamentales de la programación. Su característica más distintiva es un enfoque pedagógico innovador: utiliza palabras clave en español, pero escritas al revés. Esta particularidad busca que los principiantes puedan asociar de manera más directa los comandos con su significado original en español, al mismo tiempo que introduce un elemento lúdico y memorable en el proceso de aprendizaje. SKRN se enfoca en una sintaxis clara y sencilla para permitir a los estudiantes construir una base sólida en programación antes de pasar a lenguajes más complejos.

## Especificación Léxica
A continuación, se describen los tokens utilizados por el lenguaje SKRN y las expresiones regulares que los definen:

| **Token**           | **Expresión Regular**            | **Descripción**                          |
|---------------------|---------------------------------|------------------------------------------|
| `ID`                | `[a-zA-Z][a-zA-Z0-9]*`          | Identificadores de variables y funciones.|
| `INTEGER`           | `[0-9]+`                        | Números enteros.                        |
| `FLOATING`          | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` | Números de punto flotante.               |
| `ASSIGN`            | `=`                             | Operador de asignación.                  |
| `PLUS`              | `\+`                            | Operador de suma.                        |
| `MINUS`             | `-`                             | Operador de resta.                       |
| `TIMES`             | `\*`                            | Operador de multiplicación.              |
| `DIVIDE`            | `/`                             | Operador de división.                    |
| `MODULO`            | `%`                             | Operador de módulo.                      |
| `INCREMENT`         | `\+\+`                          | Operador de incremento.                  |
| `DECREMENT`         | `--`                            | Operador de decremento.                  |
| `EQUAL`             | `==`                            | Operador de comparación (igualdad).      |
| `NOT_EQUAL`         | `!=`                            | Operador de comparación (desigualdad).   |
| `LESS`              | `<`                             | Operador menor que.                      |
| `GREATER`           | `>`                             | Operador mayor que.                      |
| `LOGICAL_AND`       | `&&`                            | Operador lógico `AND`.                   |
| `LOGICAL_OR`        | `ll`                            | Operador lógico `OR`.                    |
| `LOGICAL_NOT`       | `!`                             | Operador lógico `NOT`.                   |
| `LPAREN`            | `\(`                            | Paréntesis izquierdo.                    |
| `RPAREN`            | `\)`                            | Paréntesis derecho.                      |
| `LBRACE`            | `{`                             | Llave izquierda.                         |
| `RBRACE`            | `}`                             | Llave derecha.                           |
| `SEMICOLON`         | `;`                             | Fin de instrucción.                      |
| `COMMA`             | `,`                             | Separador de elementos.                  |
| `type_int`          | `tni`                           | Tipo de dato entero.                     |
| `type_float`        | `taolf`                         | Tipo de dato flotante.                   |
| `type_void`         | `diov`                          | Tipo vacío (sin retorno).                |
| `IF`                | `fi`                            | Estructura condicional `if`.             |
| `ELSE`              | `esle`                          | Condición alternativa `else`.            |
| `FOR`               | `rof`                           | Bucle `for`.                             |
| `WHILE`             | `elihw`                         | Bucle `while`.                           |
| `DO`                | `od`                            | Inicio del bloque `do-while`.            |
| `RETURN`            | `nruter`                        | Retornar un valor en una función.        |
| `CLASS`             | `ssalc`                         | Definición de una clase.                 |
| `STRUCT`            | `tcurts`                        | Definición de una estructura.            |

*Nota: Algunas expresiones regulares como `+`, `*`, `++` han sido escapadas (`\+`, `\*`, `\+\+`) para su correcta visualización en Markdown y para representar su literalidad en la expresión regular.*

## Gramática
La gramática del lenguaje SKRN ha sido diseñada para ser no ambigua y factorizada por la izquierda, permitiendo su análisis mediante un parser LL(1). A continuación se presenta la gramática completa:

```
Program    -> Stmt Program | ε
Stmt       -> FuncDecl | ExprStmt | PrintStmt | ForStmt | IfStmt
             | WhileStmt | DoWhileStmt | VarDecl | ReturnStmt
Block       -> { Program }
DoWhileStmt -> od Block elihw ( E )
WhileStmt   -> elihw ( E ) Block
ForStmt     -> rof ( OptExpr ; OptExpr ; OptExpr ) Block
OptExpr     -> E | ε
IfStmt      -> fi ( E ) Block IfStmtail
IfStmtail   -> esle Block | ε
FuncDecl    -> fed id ( Params ) { Program }
Params      -> Param ParamsTail | ε
ParamsTail  -> , Param ParamsTail | ε
Param       -> id
ExprStmt    -> E
PrintStmt   -> tnirp( Args )
Args        -> E ArgsTail | Type E | ε
ArgsTail    -> , E ArgsTail | ε
VarDecl     -> Type E
Type        -> tni | taolf | diov
ReturnStmt  -> nruter E
E           -> T E'
E'          -> + T E' | - T E' | ε
T           -> G T'
T'          -> * G T' | / G T' | ε
G           -> F G'
G'          -> >= F G' | % F G' | < F G' | <= F G' | > F G'
             | = F G' | += F G' | -= F G' | == F G' | != F G' | && F G' | ε
F           -> ( E ) | id | " id " | id( Args ) B | num | eurt | eslaf
B           -> ε | Block
```

Para la validación y desarrollo de esta gramática, se utilizaron técnicas estándar de diseño de gramáticas LL(1) y se generó una tabla de análisis sintáctico (se puede encontrar una muestra en el informe completo del proyecto o en el archivo `tabla.csv` si está disponible en el repositorio). El archivo `tabla.py` es el script responsable de generar dicha tabla a partir de una definición textual de la gramática.

## Implementación
El compilador SKRN está diseñado para procesar código fuente escrito en el lenguaje SKRN y traducirlo a código ensamblador SPIM. El proceso de compilación se divide en varias fases clave, cada una responsable de una tarea específica, desde el análisis del texto fuente hasta la generación del código objeto. El sistema está preparado para identificar y reportar errores en cada una de estas etapas.

### Entrada
El compilador toma como entrada un archivo de texto (por ejemplo, `entrada_lex.txt` según se menciona en la documentación de desarrollo) que contiene el código fuente escrito en el lenguaje de programación SKRN.

### Salida
La salida final del compilador es un archivo con código en lenguaje ensamblador SPIM, listo para ser ejecutado en un simulador SPIM.

### Fases del Compilador
El desarrollo actual, según la documentación proporcionada, se ha centrado significativamente en las fases de análisis léxico y sintáctico.

#### Analizador Léxico
El análisis léxico es la primera fase del compilador. Se encarga de leer el código fuente como una secuencia de caracteres y convertirlo en una secuencia de componentes léxicos, conocidos como *tokens*.
*   **Implementación**: El módulo `lexer.py` se ha desarrollado utilizando la herramienta `ply.lex`.
*   **Funcionamiento**: Procesa el archivo de entrada (ej: `entrada_lex.txt`) y genera la secuencia de tokens definidos en la [Especificación Léxica](#especificación-léxica).

#### Analizador Sintáctico
Una vez que el código fuente ha sido descompuesto en tokens, el analizador sintáctico verifica si esta secuencia de tokens sigue la estructura gramatical definida por el lenguaje SKRN. El resultado principal de esta fase es un Árbol de Sintaxis Abstracta (AST) que representa la estructura jerárquica del código.
*   **Implementación**: El módulo `parser.py` contiene la lógica del analizador sintáctico predictivo LL(1).
*   **Tabla LL(1)**: Utiliza una tabla de análisis sintáctico LL(1) (ej: `tabla.csv`), la cual es generada por el script `tabla.py` a partir de la [Gramática](#gramática) del lenguaje.
*   **Visualización del Árbol**: El analizador construye el árbol sintáctico y tiene la capacidad de exportarlo en formato Graphviz para su visualización, lo que es crucial para la depuración y comprensión del proceso de análisis. (Ej: `generar_arbol_graphviz(root)`).

#### Analizador Semántico
Esta fase toma el árbol sintáctico como entrada y realiza comprobaciones para asegurar que el código no solo sea sintácticamente correcto, sino también semánticamente coherente.
*   **Verificación de Tipos**: Comprueba la compatibilidad de tipos en las expresiones y asignaciones. Por ejemplo, no permitir sumar un entero con una cadena directamente.
*   **Análisis de Alcance (Scope)**: Verifica que todas las variables y funciones estén declaradas antes de ser usadas y que se utilicen dentro de su ámbito correcto.
*   *(La documentación provista se enfoca en las etapas léxica y sintáctica; los detalles específicos de la implementación del analizador semántico se deducen de los requisitos generales de un compilador.)*

#### Generación de Código
Es la fase final donde el árbol sintáctico (ya verificado semánticamente) se traduce al lenguaje destino, en este caso, ensamblador SPIM.
*   **Expresiones Aritméticas y Lógicas**: Generación de instrucciones SPIM para operaciones como suma, resta, multiplicación, división, comparaciones, AND, OR, NOT.
*   **Estructuras de Control**:
    *   **If-Else**: Implementación de saltos condicionales e incondicionales en SPIM para manejar las bifurcaciones `fi` (if) y `esle` (else), incluyendo estructuras anidadas.
    *   **Bucles**: Traducción de bucles `elihw` (while), `rof` (for) y `od-elihw` (do-while) a secuencias de instrucciones SPIM con las etiquetas y saltos correspondientes.
*   **Funciones**:
    *   **Llamadas y Retornos**: Manejo de la pila (stack) para argumentos, variables locales y direcciones de retorno.
    *   **Recursividad**: Asegurar que la convención de llamadas y el manejo de la pila soporten correctamente las llamadas recursivas.
*   *(Se espera que el alumno demuestre el funcionamiento del código ensamblador generado para cada una de estas características.)*

### Manejo de Errores
El compilador debe ser capaz de detectar errores en las diferentes fases:
*   **Errores Léxicos**: Caracteres no válidos o tokens mal formados.
*   **Errores Sintácticos**: Código que no sigue la gramática del lenguaje (ej: falta un punto y coma, paréntesis no balanceados).
*   **Errores Semánticos**: Uso de variables no declaradas, incompatibilidad de tipos, errores de ámbito.
El compilador deberá reportar estos errores de una manera clara, indicando preferiblemente la naturaleza del error y su ubicación en el código fuente.

### Enlace al Repositorio
El código fuente completo de este proyecto está disponible en GitHub:
[https://github.com/JuanHuamaniVasquez/Compilador.git](https://github.com/JuanHuamaniVasquez/Compilador.git)

## Conclusiones
El desarrollo de este compilador para el lenguaje SKRN ha permitido aplicar de manera práctica los conceptos teóricos fundamentales de la materia de Compiladores. Se logró implementar exitosamente un analizador léxico y un analizador sintáctico predictivo LL(1) completo, capaz de procesar el código fuente SKRN, generar los tokens correspondientes, y construir un árbol sintáctico que puede ser visualizado mediante Graphviz.

Este proyecto sienta las bases para la implementación de las fases subsecuentes, como el análisis semántico detallado y la generación completa de código ensamblador SPIM, cumpliendo con los objetivos de aprendizaje del curso y proporcionando una herramienta con un enfoque pedagógico particular gracias a la sintaxis invertida del lenguaje SKRN.

## Estructura del Repositorio
A continuación, se describe la posible estructura de archivos clave del proyecto (esta sección puede necesitar ajustes según la organización final del repositorio):

*   `lexer.py`: Contiene la implementación del analizador léxico utilizando `ply.lex`. Es responsable de tokenizar el código fuente de SKRN.
*   `parser.py`: Implementa el analizador sintáctico predictivo LL(1). Utiliza la tabla de parsing para construir el árbol sintáctico y puede generar una representación visual del mismo (Graphviz).
*   `tabla.py`: Script utilizado para generar la tabla de análisis sintáctico LL(1) (ej. `tabla.csv` o `producciones.csv`) a partir de la gramática del lenguaje SKRN.
*   `entrada_lex.txt` (o similar): Archivo de ejemplo que contiene código fuente en lenguaje SKRN, utilizado como entrada para el compilador.
*   `tabla.csv` / `producciones.csv` (o similar): Archivo CSV que almacena la tabla de análisis sintáctico LL(1) generada por `tabla.py`.
*   `README.md`: Este archivo, que contiene la documentación del proyecto.
*   (Otros archivos como ejemplos de código SKRN, scripts de prueba, o el informe en LaTeX podrían estar en directorios dedicados como `examples/`, `tests/`, `docs/` respectivamente).

## Cómo Ejecutar
Para compilar y ejecutar el compilador de SKRN, sigue estos pasos generales. Asegúrate de tener Python y las dependencias necesarias instaladas.

### 1. Prerrequisitos
*   **Python 3.x**
*   **PLY (Python Lex-Yacc)**: Utilizado para el análisis léxico y sintáctico. Puedes instalarlo con pip:
    ```bash
    pip install ply
    ```
*   **Graphviz**: Necesario para visualizar el árbol sintáctico (opcional si solo se desea la compilación sin visualización). Asegúrate de que los ejecutables de Graphviz estén en el PATH de tu sistema.
    *   Puedes descargarlo desde [graphviz.org](https://graphviz.org/download/).
    *   En sistemas basados en Debian/Ubuntu: `sudo apt-get install graphviz`
    *   En macOS con Homebrew: `brew install graphviz`

### 2. Preparación (si es necesario)
*   **Generar la Tabla de Análisis Sintáctico**: Si la tabla LL(1) (ej. `tabla.csv` o `producciones.csv`) no está incluida o necesita ser regenerada a partir de la gramática:
    ```bash
    python tabla.py
    ```
    Esto debería generar el archivo CSV con la tabla de parsing.

### 3. Ejecución del Compilador (Fases de Análisis)
El documento LaTeX describe la ejecución del parser con un conjunto de tokens de entrada. Para probar el flujo completo desde un archivo de código SKRN:

*   **Paso 1: Obtener tokens (usando `lexer.py`)**
    *   El `lexer.py` está diseñado para procesar un archivo de entrada (ej. `entrada_lex.txt`). Deberás adaptar o usar su funcionalidad para alimentar al `parser.py`.
*   **Paso 2: Análisis Sintáctico y Generación del Árbol (usando `parser.py`)**
    *   El `parser.py` toma la secuencia de tokens y, utilizando la tabla de parsing (ej. `producciones.csv`), construye el árbol sintáctico.
    *   Un ejemplo de cómo se podría invocar (basado en el LaTeX, adaptado para tomar tokens del lexer):
        ```python
        # En parser.py (o un script principal)
        # from lexer import get_tokens_from_file # Suponiendo una función en lexer.py
        # from parser_module import predictive_parser, generar_arbol_graphviz # Suponiendo funciones en parser.py

        # input_file = 'ruta/a/tu/codigo.skrn' # o 'entrada_lex.txt'
        # tokens = get_tokens_from_file(input_file)

        # # Si el lexer ya está integrado en el parser o se llama desde ahí:
        # root_node = predictive_parser(tokens, csv_file='producciones.csv') # o tabla.csv
        # if root_node:
        #     generar_arbol_graphviz(root_node, "nombre_del_arbol") # Genera un archivo .dot y .png
        #     print("Árbol sintáctico generado como nombre_del_arbol.png")
        # else:
        #     print("Error durante el análisis sintáctico.")
        ```
    *   Ejecuta el script del parser (o el script principal que lo utilice):
        ```bash
        python parser.py
        ```
        (Asegúrate de que `parser.py` esté configurado para leer de un archivo de entrada o que tengas un script que maneje la secuencia.)

### 4. Generación de Código SPIM (Fase Futura/No Detallada en LaTeX)
*   Una vez que las fases de análisis semántico y generación de código estén implementadas, se ejecutaría un paso adicional que tomaría el árbol sintáctico (o una representación intermedia) para producir el código ensamblador SPIM.
    ```bash
    # Ejemplo conceptual
    # python compilador_skrn.py --archivo_entrada codigo.skrn --archivo_salida codigo.asm
    ```

### 5. Probar el Código Ensamblador
*   Utiliza un simulador SPIM (como QtSpim) para cargar y ejecutar el archivo `.asm` generado.
*   Verifica que el comportamiento del programa en SPIM sea el esperado según el código fuente SKRN.

**Nota:** Las instrucciones anteriores se basan en la información del documento LaTeX, que se centra en el análisis léxico y sintáctico. Deberás adaptar los comandos y scripts según la estructura final y el flujo de trabajo de tu proyecto completo, especialmente para la integración de todas las fases y la generación de código SPIM.

---
*Este README sigue la estructura y los puntos solicitados en la rúbrica del proyecto final de Compiladores.*

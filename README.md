# 🖥️ **Lenguaje de Programación SKRN**  

## 👨‍💻 **Integrantes**  
- **Hugo Alonso Youzzueff Diaz Chavez**  
- **Juan José Huamaní Vásquez**  
- **Melvin Jarred Yabar Carazas**  
- **Gabriel Frank Krisna Zela Flores**  

## 🎓 **Docente**  
- **Vicente Enrique Machaca Arceda**  

📅 **Fecha:** *20/03/2025*  

---

## 🚀 **Nombre del Lenguaje**  
**SKRN**  

## 🎯 **Justificación y Descripción**  

**SKRN** es un lenguaje de programación diseñado para facilitar el aprendizaje de conceptos fundamentales en programación. Se distingue por su enfoque innovador: utiliza palabras clave en español escritas al revés, lo que permite a los principiantes asociar más fácilmente los comandos con su significado original.  

### 🔹 **Características Claves**  
✔ Inspirado en Python y C, combinando facilidad de uso con eficiencia en el control de recursos.  
✔ Uso de palabras clave en español invertidas para mejorar la comprensión.  
✔ Soporte para estructuras de control, funciones y programación orientada a objetos.  
✔ Inferencia de tipos implícita para simplificar el desarrollo.  

---

## 📌 **Estructura General del Lenguaje**  

El lenguaje **SKRN** sigue una sintaxis simple basada en estructuras de programación imperativa.  

### 📝 **Ejemplo de Código**  

```skrn
fi (x > 0) {
    nruter x;
} esle {
    nruter -x;
}
```

📌 **Explicación:**  
- `fi` actúa como el condicional `if`.  
- `esle` representa `else`.  
- `nruter` es el equivalente a `return`.  

---

## 🔢 **Tabla de Tokens**  

| **Token**           | **Expresión Regular**            | **Descripción**                          |
|---------------------|---------------------------------|------------------------------------------|
| **ID**             | `[a-zA-Z][a-zA-Z0-9]*`          | Identificadores de variables y funciones. |
| **INTEGER**        | `[0-9]+`                        | Números enteros.                        |
| **FLOATING**       | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` | Números de punto flotante.               |
| **ASSIGN**         | `=`                             | Operador de asignación.                  |
| **PLUS**          | `+`                             | Operador de suma.                        |
| **MINUS**         | `-`                             | Operador de resta.                       |
| **TIMES**         | `*`                             | Operador de multiplicación.              |
| **DIVIDE**        | `/`                             | Operador de división.                    |
| **MODULO**        | `%`                             | Operador de módulo.                      |
| **INCREMENT**     | `++`                            | Operador de incremento.                  |
| **DECREMENT**     | `--`                            | Operador de decremento.                  |
| **EQUAL**        | `==`                            | Operador de comparación (igualdad).      |
| **NOT_EQUAL**     | `!=`                            | Operador de comparación (desigualdad).   |
| **LESS**         | `<`                             | Operador menor que.                      |
| **GREATER**      | `>`                             | Operador mayor que.                      |
| **LOGICAL_AND**   | `&&`                            | Operador lógico `AND`.                   |
| **LOGICAL_OR**    | `ll`                            | Operador lógico `OR`.                    |
| **LOGICAL_NOT**   | `!`                             | Operador lógico `NOT`.                   |
| **LPAREN**        | `\(`                            | Paréntesis izquierdo.                    |
| **RPAREN**        | `\)`                            | Paréntesis derecho.                      |
| **LBRACE**        | `{`                             | Llave izquierda.                         |
| **RBRACE**        | `}`                             | Llave derecha.                           |
| **SEMICOLON**     | `;`                             | Fin de instrucción.                      |
| **COMMA**         | `,`                             | Separador de elementos.                  |
| **type_int**      | `tni`                           | Tipo de dato entero.                     |
| **type_float**    | `taolf`                         | Tipo de dato flotante.                   |
| **type_void**     | `diov`                          | Tipo vacío (sin retorno).                |
| **IF**           | `fi`                            | Estructura condicional `if`.             |
| **ELSE**         | `esle`                          | Condición alternativa `else`.            |
| **FOR**          | `rof`                           | Bucle `for`.                             |
| **WHILE**        | `elihw`                         | Bucle `while`.                           |
| **DO**           | `od`                            | Inicio del bloque `do-while`.            |
| **RETURN**       | `nruter`                        | Retornar un valor en una función.        |
| **CLASS**        | `ssalc`                         | Definición de una clase.                 |
| **STRUCT**       | `tcurts`                        | Definición de una estructura.            |

---

## 🔥 **Ejemplos de Código en SKRN**  

### 🖥️ (1) **Hola Mundo** 🌎  
```skrn
tni niam() {
    tuoc << "Hola, Mundo!";
    nruter 0;
}
```

📌 **Explicación:**  
- `niam` es la función principal (`main`).  
- `tuoc` representa la salida estándar (`cout`).  
- `nruter 0` finaliza el programa correctamente.  

---

### 🔄 (2) **Bucles Anidados** 🔄  
```skrn
tni niam() {
    tni i = 0;
    elihw (i < 5) od {
        tni j = 0;
        elihw (j < 5) od {
            tuoc << i << " " << j << endl;
            j = j + 1;
        }
        i = i + 1;
    }
    nruter 0;
}
```

📌 **Explicación:**  
- Se utilizan `elihw` (`while`) para iterar hasta que la condición se cumpla.  
- `od` marca el inicio del bloque del bucle.  
- `tuoc` imprime valores en pantalla.  

---

### 🧮 (3) **Recursividad (Factorial)** 🧮  
```skrn
tni factorial(tni n) {
    fi (n == 0) {
        nruter 1;
    }
    nruter n * factorial(n - 1);
}

tni niam() {
    tni resultado = factorial(5);
    tuoc << resultado << endl;
    nruter 0;
}
```

📌 **Explicación:**  
- `factorial` es una función recursiva que calcula el factorial de un número.  
- Si `n == 0`, se devuelve `1`.  
- Si no, se retorna `n * factorial(n - 1)`.  

---

## 🚀 **Conclusión**  
**SKRN** Su estructura clara y su innovador uso de palabras clave invertidas lo convierten en una excelente opción para principiantes que desean aprender programación de manera intuitiva y eficiente.  

🔹 **Fácil de aprender** gracias a su relación con palabras clave en español.  
🔹 **Potente y flexible**, permitiendo desde estructuras básicas hasta programación orientada a objetos.  

🔥 **¡Explora SKRN y descubre una nueva forma de aprender a programar!** 🎉  

---

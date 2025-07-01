.data
a: .word 0
b: .word 0
c: .word 0
d: .word 0

.text
main:
    # Cargar valor de variable a
    lw $t0, a
    # Cargar constante 3
    li $t1, 3
    # Operación = entre $t0 y $t1
    # Cargar constante 4
    li $t3, 4
    # Operación + entre  y
    add $t4, ,
    # Guardar resultado en variable a
    sw $t4, a
    # Cargar valor de variable b
    lw $t5, b
    # Cargar constante 8
    li $t6, 8
    # Operación = entre $t5 y $t6
    # Cargar constante 9
    li $t8, 9
    # Cargar constante 5
    li $t9, 5
    # Operación * entre  y
    mul $t0, ,
    # Guardar resultado en variable b
    sw $t1, b
    # Cargar constante 9
    li $t2, 9
    # Asignar valor directo a 'c'
    sw $t2, c
    # Cargar valor de variable d
    lw $t3, d
    # Cargar valor de variable a
    lw $t4, a
    # Operación = entre $t3 y $t4
    # Cargar valor de variable b
    lw $t6, b
    # Operación + entre  y
    add $t7, ,
    # Guardar resultado en variable d
    sw $t7, d
    li $v0, 10
    syscall
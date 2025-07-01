.data
result: .word 0

.text
.globl main
main:
    # Initialization for variable result
    # Cargar booleano true (1)
    li $t0, 1
    # Cargar booleano false (0)
    li $t1, 0
    # Operación && entre $t0 y $t1
    and $t2, $t0, $t1
    # Exit program
    li $v0, 10
    syscall
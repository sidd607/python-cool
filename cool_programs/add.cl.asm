.data
		main_y: .word 0
		main_tmp: .asciiz 
.text
	main: 
		move $fp, $sp
# Function call sequence begin
		sw $fp 0($sp) # push $fp (step 1) 
		addiu $sp $sp -4 # push $fp (step 2) 

li $a0 4
		sw $a0 0($sp) # push $a0 (step 1) 
		addiu $sp $sp -4 # push $a0 (step 2) 

li $a0 3
		sw $a0 0($sp) # push $a0 (step 1) 
		addiu $sp $sp -4 # push $a0 (step 2) 

li $a0 4
		sw $a0 0($sp) # push $a0 (step 1) 
		addiu $sp $sp -4 # push $a0 (step 2) 

jal main_add
# Function call sequence ends
		li $v0, 10
		syscall
	main_add:
		move $fp $sp 
		sw $ra 0($sp) # push $ra (step 1) 
		addiu $sp $sp -4 # push $ra (step 2) 

#starting binary operation
#starting binary operation
lw $a0 4($fp)

		sw $a0 0($sp) # push $a0 (step 1) 
		addiu $sp $sp -4 # push $a0 (step 2) 

lw $a0 4($fp)

		lw $t1 4($sp) # pop $t1 (step 1) 
		addiu $sp $sp 4 # pop $t1 (step 2) 

addu $a0 $a0 $t1
		sw $a0 0($sp) # push $a0 (step 1) 
		addiu $sp $sp -4 # push $a0 (step 2) 

lw $a0 4($fp)

		lw $t1 4($sp) # pop $t1 (step 1) 
		addiu $sp $sp 4 # pop $t1 (step 2) 

addu $a0 $a0 $t1
		lw $ra 4($sp) # pop $ra (step 1) 
		addiu $sp $sp 4 # pop $ra (step 2) 
move $sp $fp # restore stack pointer to the beginning of the current stack frame
 lw $fp 0($sp) # restore frame pointer to its previous value
 jr $ra # jump back to the caller


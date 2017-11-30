                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Bool..vtable:           ;; virtual function table for Bool
                        constant string1
                        constant Bool..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO..vtable:             ;; virtual function table for IO
                        constant string2
                        constant IO..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        constant IO.in_int
                        constant IO.in_string
                        constant IO.out_int
                        constant IO.out_string
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Int..vtable:            ;; virtual function table for Int
                        constant string3
                        constant Int..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Main..vtable:           ;; virtual function table for Main
                        constant string4
                        constant Main..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        constant IO.in_int
                        constant IO.in_string
                        constant IO.out_int
                        constant IO.out_string
                        constant Main.main
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Object..vtable:         ;; virtual function table for Object
                        constant string5
                        constant Object..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
String..vtable:         ;; virtual function table for String
                        constant string6
                        constant String..new
                        constant Object.abort
                        constant Object.copy
                        constant Object.type_name
                        constant String.concat
                        constant String.length
                        constant String.substr
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Bool..new:              ;; constructor for Bool
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 4
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 0
                        st r0[0] <- r2
                        li r2 <- 4
                        st r0[1] <- r2
                        la r2 <- Bool..vtable
                        st r0[2] <- r2
                        ;; initialize attributes
                        ;; self[3] holds field (raw content) (Int)
                        li r1 <- 0
                        st r0[3] <- r1
                        ;; self[3] (raw content) initializer -- none 
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO..new:                ;; constructor for IO
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 3
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 10
                        st r0[0] <- r2
                        li r2 <- 3
                        st r0[1] <- r2
                        la r2 <- IO..vtable
                        st r0[2] <- r2
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Int..new:               ;; constructor for Int
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 4
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 1
                        st r0[0] <- r2
                        li r2 <- 4
                        st r0[1] <- r2
                        la r2 <- Int..vtable
                        st r0[2] <- r2
                        ;; initialize attributes
                        ;; self[3] holds field (raw content) (Int)
                        li r1 <- 0
                        st r0[3] <- r1
                        ;; self[3] (raw content) initializer -- none 
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Main..new:              ;; constructor for Main
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 3
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 11
                        st r0[0] <- r2
                        li r2 <- 3
                        st r0[1] <- r2
                        la r2 <- Main..vtable
                        st r0[2] <- r2
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Object..new:            ;; constructor for Object
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 3
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 12
                        st r0[0] <- r2
                        li r2 <- 3
                        st r0[1] <- r2
                        la r2 <- Object..vtable
                        st r0[2] <- r2
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
String..new:            ;; constructor for String
                        mov fp <- sp
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        li r0 <- 4
                        alloc r0 r0
                        ;; store class tag, object size and vtable pointer
                        li r2 <- 3
                        st r0[0] <- r2
                        li r2 <- 4
                        st r0[1] <- r2
                        la r2 <- String..vtable
                        st r0[2] <- r2
                        ;; initialize attributes
                        ;; self[3] holds field (raw content) (String)
                        la r1 <- the.empty.string
                        st r0[3] <- r1
                        ;; self[3] (raw content) initializer -- none 
                        mov r1 <- r0
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Object.abort:           ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        la r1 <- string7
                        syscall IO.out_string
                        syscall exit
Object.abort.end:       ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Object.copy:            ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ld r2 <- r0[1]
                        alloc r1 r2
                        push r1
l1:                     bz r2 l2
                        ld r3 <- r0[0]
                        st r1[0] <- r3
                        li r3 <- 1
                        add r0 <- r0 r3
                        add r1 <- r1 r3
                        li r3 <- 1
                        sub r2 <- r2 r3
                        jmp l1
l2:                     ;; done with Object.copy loop
                        pop r1
Object.copy.end:        ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Object.type_name:       ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ;; new String
                        push fp
                        push r0
                        la r2 <- String..new
                        call r2
                        pop r0
                        pop fp
                        ;; obtain vtable for self object
                        ld r2 <- r0[2]
                        ;; look up type name at offset 0 in vtable
                        ld r2 <- r2[0]
                        st r1[3] <- r2
Object.type_name.end:   ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO.in_int:              ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ;; new Int
                        push fp
                        push r0
                        la r2 <- Int..new
                        call r2
                        pop r0
                        pop fp
                        mov r2 <- r1
                        syscall IO.in_int
                        st r2[3] <- r1
                        mov r1 <- r2
IO.in_int.end:          ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO.in_string:           ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ;; new String
                        push fp
                        push r0
                        la r2 <- String..new
                        call r2
                        pop r0
                        pop fp
                        mov r2 <- r1
                        syscall IO.in_string
                        st r2[3] <- r1
                        mov r1 <- r2
IO.in_string.end:       ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO.out_int:             ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; fp[2] holds argument x (Int)
                        ;; method body begins
                        ld r2 <- fp[2]
                        ld r1 <- r2[3]
                        syscall IO.out_int
                        mov r1 <- r0
IO.out_int.end:         ;; method body ends
                        pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
IO.out_string:          ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; fp[2] holds argument x (String)
                        ;; method body begins
                        ld r2 <- fp[2]
                        ld r1 <- r2[3]
                        syscall IO.out_string
                        mov r1 <- r0
IO.out_string.end:      ;; method body ends
                        pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Main.main:              ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ;; out_string(...)
                        push r0
                        push fp
                        ;; new String
                        push fp
                        push r0
                        la r2 <- String..new
                        call r2
                        pop r0
                        pop fp
                        ;; string8 holds "Hello World\n"
                        la r2 <- string8
                        st r1[3] <- r2
                        push r1
                        push r0
                        ;; obtain vtable for self object of type Main
                        ld r2 <- r0[2]
                        ;; look up out_string() at offset 8 in vtable
                        ld r2 <- r2[8]
                        call r2
                        pop fp
                        pop r0
Main.main.end:          ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
String.concat:          ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; fp[2] holds argument s (String)
                        ;; method body begins
                        ;; new String
                        push fp
                        push r0
                        la r2 <- String..new
                        call r2
                        pop r0
                        pop fp
                        mov r3 <- r1
                        ld r2 <- fp[2]
                        ld r2 <- r2[3]
                        ld r1 <- r0[3]
                        syscall String.concat
                        st r3[3] <- r1
                        mov r1 <- r3
String.concat.end:      ;; method body ends
                        pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
String.length:          ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; method body begins
                        ;; new Int
                        push fp
                        push r0
                        la r2 <- Int..new
                        call r2
                        pop r0
                        pop fp
                        mov r2 <- r1
                        ld r1 <- r0[3]
                        syscall String.length
                        st r2[3] <- r1
                        mov r1 <- r2
String.length.end:      ;; method body ends
                        pop ra
                        li r2 <- 1
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
String.substr:          ;; method definition
                        mov fp <- sp
                        pop r0
                        ;; stack room for temporaries: 1
                        li r2 <- 1
                        sub sp <- sp r2
                        push ra
                        ;; fp[3] holds argument i (Int)
                        ;; fp[2] holds argument l (Int)
                        ;; method body begins
                        ;; new String
                        push fp
                        push r0
                        la r2 <- String..new
                        call r2
                        pop r0
                        pop fp
                        mov r3 <- r1
                        ld r2 <- fp[2]
                        ld r2 <- r2[3]
                        ld r1 <- fp[3]
                        ld r1 <- r1[3]
                        ld r0 <- r0[3]
                        syscall String.substr
                        bnz r1 l3
                        la r1 <- string9
                        syscall IO.out_string
                        syscall exit
l3:                     st r3[3] <- r1
                        mov r1 <- r3
String.substr.end:      ;; method body ends
                        pop ra
                        li r2 <- 3
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
                        ;; global string constants
the.empty.string:       constant ""
string1:                constant "Bool"
string2:                constant "IO"
string3:                constant "Int"
string4:                constant "Main"
string5:                constant "Object"
string6:                constant "String"
string7:                constant "abort\n"
string8:                constant "Hello World\n"
string9:                constant "ERROR: 0: Exception: String.substr out of range\n"
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
eq_handler:             ;; helper function for =
                        mov fp <- sp
                        pop r0
                        push ra
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        beq r1 r2 eq_true
                        li r3 <- 0
                        beq r1 r3 eq_false
                        beq r2 r3 eq_false
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        ;; place the sum of the type tags in r1
                        add r1 <- r1 r2
                        li r2 <- 0
                        beq r1 r2 eq_bool
                        li r2 <- 2
                        beq r1 r2 eq_int
                        li r2 <- 6
                        beq r1 r2 eq_string
                        ;; otherwise, use pointer comparison
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        beq r1 r2 eq_true
eq_false:               ;; not equal
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        jmp eq_end
eq_true:                ;; equal
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        li r2 <- 1
                        st r1[3] <- r2
                        jmp eq_end
eq_bool:                ;; two Bools
eq_int:                 ;; two Ints
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        beq r1 r2 eq_true
                        jmp eq_false
eq_string:              ;; two Strings
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        beq r1 r2 eq_true
                        jmp eq_false
eq_end:                 pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
le_handler:             ;; helper function for <=
                        mov fp <- sp
                        pop r0
                        push ra
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        beq r1 r2 le_true
                        li r3 <- 0
                        beq r1 r3 le_false
                        beq r2 r3 le_false
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        ;; place the sum of the type tags in r1
                        add r1 <- r1 r2
                        li r2 <- 0
                        beq r1 r2 le_bool
                        li r2 <- 2
                        beq r1 r2 le_int
                        li r2 <- 6
                        beq r1 r2 le_string
                        ;; for non-primitives, equality is our only hope
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        beq r1 r2 le_true
le_false:               ;; not less-than-or-equal
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        jmp le_end
le_true:                ;; less-than-or-equal
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        li r2 <- 1
                        st r1[3] <- r2
                        jmp le_end
le_bool:                ;; two Bools
le_int:                 ;; two Ints
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        ble r1 r2 le_true
                        jmp le_false
le_string:              ;; two Strings
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        ble r1 r2 le_true
                        jmp le_false
le_end:                 pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
lt_handler:             ;; helper function for <
                        mov fp <- sp
                        pop r0
                        push ra
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        li r3 <- 0
                        beq r1 r3 lt_false
                        beq r2 r3 lt_false
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        ;; place the sum of the type tags in r1
                        add r1 <- r1 r2
                        li r2 <- 0
                        beq r1 r2 lt_bool
                        li r2 <- 2
                        beq r1 r2 lt_int
                        li r2 <- 6
                        beq r1 r2 lt_string
                        ;; for non-primitives, < is always false
lt_false:               ;; not less than
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        jmp lt_end
lt_true:                ;; less than
                        ;; new Bool
                        push fp
                        push r0
                        la r2 <- Bool..new
                        call r2
                        pop r0
                        pop fp
                        li r2 <- 1
                        st r1[3] <- r2
                        jmp lt_end
lt_bool:                ;; two Bools
lt_int:                 ;; two Ints
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        blt r1 r2 lt_true
                        jmp lt_false
lt_string:              ;; two Strings
                        ld r1 <- fp[3]
                        ld r2 <- fp[2]
                        ld r1 <- r1[3]
                        ld r2 <- r2[3]
                        ld r1 <- r1[0]
                        ld r2 <- r2[0]
                        blt r1 r2 lt_true
                        jmp lt_false
lt_end:                 pop ra
                        li r2 <- 2
                        add sp <- sp r2
                        return
                        ;; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
start:                  ;; program begins here
                        la r2 <- Main..new
                        push fp
                        call r2
                        push fp
                        push r1
                        la r2 <- Main.main
                        call r2
                        syscall exit

	.arch armv8-a
	.file	"esto_no_es_atomico.c"
	.text
	.section	.rodata
	.align	3
.LC0:
	.string	"Va una operaci\303\263n no at\303\263mica: La suma de %d, %d, %d, %d: %d\n"
	.align	3
.LC1:
	.string	"Es m\303\241s: \302\241Ni siquiera el post-incremento es (siempre) at\303\263mico!"
	.text
	.align	2
	.global	main
	.type	main, %function
main:
.LFB0:
	.cfi_startproc
	stp	x29, x30, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 29, -32
	.cfi_offset 30, -24
	mov	x29, sp
	mov	w0, 5
	str	w0, [sp, 28]
	mov	w0, 7
	str	w0, [sp, 24]
	mov	w0, 3
	str	w0, [sp, 20]
	mov	w0, 8
	str	w0, [sp, 16]
	ldr	w1, [sp, 28]
	ldr	w0, [sp, 24]
	add	w1, w1, w0
	ldr	w0, [sp, 20]
	add	w1, w1, w0
	ldr	w0, [sp, 16]
	add	w0, w1, w0
	mov	w5, w0
	ldr	w4, [sp, 16]
	ldr	w3, [sp, 20]
	ldr	w2, [sp, 24]
	ldr	w1, [sp, 28]
	adrp	x0, .LC0
	add	x0, x0, :lo12:.LC0
	bl	printf
	adrp	x0, .LC1
	add	x0, x0, :lo12:.LC1
	bl	puts
	ldr	w0, [sp, 28]
	add	w0, w0, 1
	str	w0, [sp, 28]
	nop
	ldp	x29, x30, [sp], 32
	.cfi_restore 30
	.cfi_restore 29
	.cfi_def_cfa_offset 0
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Debian 12.2.0-14) 12.2.0"
	.section	.note.GNU-stack,"",@progbits

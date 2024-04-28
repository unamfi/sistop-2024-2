	.file	"esto_no_es_atomico.c"
	.text
	.section	.rodata
	.align 8
.LC0:
	.string	"Va una operaci\303\263n no at\303\263mica: La suma de %d, %d, %d, %d: %d\n"
	.align 8
.LC1:
	.string	"Es m\303\241s: \302\241Ni siquiera el post-incremento es (siempre) at\303\263mico!"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$5, -4(%rbp)
	movl	$7, -8(%rbp)
	movl	$3, -12(%rbp)
	movl	$8, -16(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	addl	%eax, %edx
	movl	-12(%rbp), %eax
	addl	%eax, %edx
	movl	-16(%rbp), %eax
	leal	(%rdx,%rax), %edi
	movl	-16(%rbp), %esi
	movl	-12(%rbp), %ecx
	movl	-8(%rbp), %edx
	movl	-4(%rbp), %eax
	movl	%edi, %r9d
	movl	%esi, %r8d
	movl	%eax, %esi
	leaq	.LC0(%rip), %rax
	movq	%rax, %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	.LC1(%rip), %rax
	movq	%rax, %rdi
	call	puts@PLT
	addl	$1, -4(%rbp)
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Debian 13.2.0-23) 13.2.0"
	.section	.note.GNU-stack,"",@progbits

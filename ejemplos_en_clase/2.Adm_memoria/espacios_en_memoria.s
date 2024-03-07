	.file	"espacios_en_memoria.c"
	.text
	.globl	datos
	.data
	.align 4
	.type	datos, @object
	.size	datos, 4
datos:
	.long	10
	.globl	cadena
	.section	.rodata
.LC0:
	.string	"\302\241Hola bola!"
	.section	.data.rel.local,"aw"
	.align 8
	.type	cadena, @object
	.size	cadena, 8
cadena:
	.quad	.LC0
	.text
	.globl	funcioncita
	.type	funcioncita, @function
funcioncita:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	movl	$0, -4(%rbp)
	jmp	.L2
.L3:
	movl	$33, %edi
	call	putchar@PLT
	addl	$1, -4(%rbp)
.L2:
	movl	-4(%rbp), %eax
	cmpl	-20(%rbp), %eax
	jl	.L3
	movl	$10, %edi
	call	putchar@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	funcioncita, .-funcioncita
	.section	.rodata
.LC1:
	.string	"blablabl\303\241"
	.text
	.globl	main
	.type	main, @function
main:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	$15, -4(%rbp)
	leaq	.LC1(%rip), %rax
	movq	%rax, -16(%rbp)
	movl	$120, %edi
	call	malloc@PLT
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movb	$65, (%rax)
	movq	-24(%rbp), %rax
	addq	$1, %rax
	movb	$32, (%rax)
	movq	-24(%rbp), %rax
	addq	$2, %rax
	movb	$65, (%rax)
	movq	-24(%rbp), %rax
	addq	$3, %rax
	movb	$0, (%rax)
	movl	$10, %edi
	call	funcioncita
	movl	$5, %edi
	call	funcioncita
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	puts@PLT
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	main, .-main
	.ident	"GCC: (Debian 13.2.0-12) 13.2.0"
	.section	.note.GNU-stack,"",@progbits

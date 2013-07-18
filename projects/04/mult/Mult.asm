// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

	@R0
	D=M
	@MULTBYZERO
	D;JEQ
	@R1
	D=M
	@MULTBYZERO
	D;JEQ
	@i
	M=1
	@ans
	M=0

(LOOP)
	@R0
	D=M
	@ans
	M=M+D	// ans = ans + *R0
	D=M
	@R2
	M=D
	@i		// D=i
	D=M
	@R1		// A = R1
	D=D-M	// D= i - *R1
	@END
	D;JGE 	// If (i-R1) == 0 goto END
	@i
	M=M+1	// i++
	@LOOP
	0;JMP

	
(END)
	@END
	0;JMP

(MULTBYZERO)
	@R2
	M=0
	@END
	0;JMP


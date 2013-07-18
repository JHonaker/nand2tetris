// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
// Useful registers:
// 
// @SCREEN, sets the A register to the screen's top left corner. (Address 16384)
// Pixel at Row r and Column c is mapped on the c % 16 bit of the word at
// RAM[16384 + r * 32 + c/16]
// 
// @KBD is the register for keyboard input

	@SCREEN
	D=A
	@curpos
	M=D			// Set the current position of the 'cursor' to SCREEN
	
(LOOP)
	@KBD
	D=M			// If the key is down set D to 1, else 0
	@CLEAR
	D;JEQ		// If @KBD == 0 goto CLEAR
	@DRAW
	0;JMP		// else goto DRAW

(DRAW)
	@curpos
	D=M
	@24576
	D=D-A
	@LOOP
	D;JGE
	@curpos
	D=M
	A=M
	M=-1
	@curpos
	M=M+1
	@LOOP
	0;JMP

(CLEAR)
	@curpos
	D=M
	A=M
	M=0
	@SCREEN
	D=D-A
	@LOOP
	D;JLT
	@curpos
	M=M-1
	@LOOP
	0;JMP

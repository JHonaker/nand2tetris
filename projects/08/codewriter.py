# Current temporary stage one implementation of the VM Code Generator
#
# Stack Arithmetic, Logical Commands, push contstant x
# 
# Reference Note: -1 is true, 0 is false

import os
from parser import *

class CodeWriter:

    def __init__(self, outfile):
        """Opens the file output file/stream and gets
        ready to write into it."""

        isDirectory = outfile[-3:] != '.vm'

        self.outfile = open(outfile[:-3] + '.asm', 'w')
        
        # Create the current label.
        # This is machine read and wrote, so numeric labels will suffice
        self.UID = 0

        # Static label, this changes with each filename:
        # Forms the command labels @Xxx.j
        self.staticPrefix = ''

        if (isDirectory):
            for file in os.listdir('/' + outfile):
                if file.endswith(".vm"):
                    self.setFileName('./' + outfile + '/' + file)

        else:
            self.setFileName(outfile)

        self.outfile.close()
        print 'Closed file: ' + outfile[:-3] + '.asm'


    def setFileName(self, fileName):
        """Informs the code writer that the translations of
        a new VM file has started."""
        p = parser(fileName)
        self.staticPrefix = fileName.split('.')[0]

        while(p.hasMoreCommands()):
            p.advance()
            self.dispatchWriter(p.commandType(), p.currentCommand)

    def labelUID(self):
        temp = self.UID
        self.UID += 1
        return str(temp)

    # Label creating functions
    def newLabel(self):
        """Creates the next unused label."""
        return str(self.labelUID())
    
    def staticLabel(self, index):
        """Returns the static label of the index."""
        return self.staticPrefix + '.' + str(index)

    
    # Command writers and the dispatcher
    def dispatchWriter(self, commandType, command):
        """Dispatches the write for the given command type."""
        print command

        if (commandType == 'C_ARITHMETIC'):
            self.writeArithmetic(command[0])
        elif (commandType == 'C_POP' or commandType == 'C_PUSH'):
            self.writePushPop(command[0], command[1], command[2])
        elif (commandType == 'C_GOTO'):
            self.writeGoto(command[1])
        elif (commandType == 'C_IF'):
            self.writeIf(command[1])
        elif (commandType == 'C_FUNCTION'):
            pass
        elif (commandType == 'C_RETURN'):
            pass
        elif (commandType == 'C_CALL'):
            pass
        elif (commandType == 'C_LABEL'):
            self.writeLabel(command[1])
        else:
            pass

    def writeInit(self):
        """Writes assembly code that effects the VM initialization,
        also called the bootstrap code. This code must be placed at
        the beginning of the output file."""
        pass
    
    # writeLabel is just an lCommand
    def writeLabel(self, label):
        self.lCommand(label)

    def writeGoto(self, label):
        """Writes assembly code for goto statement."""
        self.aCommand(label)
        self.cCommand(dest=None, comp='0', jump='JMP') # Unconditional jump

    def writeIf(self, label):
        """Writes assembly code for the if-goto statement.
        Pops top value off stack, if != 0, jump to label.
        Otherwise, continue with next command."""
        self.decreaseStackPointer()
        self.stackToDest('D') # Pop top value off stack
        self.aCommand(label) # Load jump point
        self.cCommand(dest=None, comp='D', jump='JNE') # Jump if != 0
    
    def writeCall(self, functionName, numArgs):
        """Writes assembly code for the function: functionName
        with numArgs number of arguments."""
        return_address = self.newLabel()

        self.constToStack(return_address)
        self.increaseStackPointer()

        self.aCommand('LCL')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('ARG')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('THIS')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        self.aCommand('THAT')
        self.cCommand('D', 'M')
        self.compToStack('D')
        self.increaseStackPointer()

        # ARG = SP - numArgs - 5
        self.aCommand('SP')         # A=SP
        self.cCommand('D', 'M')     # D=M=SP
        self.aCommand(numArgs)      # A=numArgs
        self.cCommand('D', 'D-A')   # D=D-A=SP-numArgs
        self.aCommand('5')          # A=5
        self.cCommand('D', 'D-A')   # D=D-A=SP-numArgs-5

        self.aCommand('ARG')
        self.cCommand('M', 'D')

        # LCL = SP
        self.aCommand('SP')
        self.cCommand('D', 'M')
        self.aCommand('LCL')
        self.cCommand('M', 'D')
        
        # goto functionName
        self.aCommand(functionName)
        self.cCommand(None, '0', 'JMP')

        self.lCommand(return_address)


    def writeReturn(self):
        """Writes assembly code for that returns from the
        current function."""
        pass

    def writeFunction(self, functionName, numLocals):
        """Writes assembly code for the function: functionName
        with numLocals number of local variable."""
        self.writeLabel(functionName)
        for i in range(int(numLocals)):
            self.constToStack(0)
            self.increaseStackPointer()
    
    def writeArithmetic(self, command):
        """Writes the assembly code that is the given translation
        of the command given."""
        # Arithmetic
        if (command == 'add'):
            self.binaryOp('D+A')
        elif (command == 'sub'):
            self.binaryOp('A-D')
        elif (command == 'neg'):
            self.unaryOp('-D')
        # Bitwise
        elif (command == 'and'):
            self.binaryOp('D&A')
        elif (command == 'or'):
            self.binaryOp('D|A')
        elif (command == 'not'):
            self.unaryOp('!D')
        # Logical
        elif (command == 'eq'):
            self.logicalOp('JEQ')
        elif (command == 'gt'):
            self.logicalOp('JGT')
        elif (command == 'lt'):
            self.logicalOp('JLT')

    def writePushPop(self, command, segment, index):
        """Writes the assembly code that is the translation of the
        given command, where command is either C_PUSH or C_POP."""
        if (command == 'push'):

            if (segment == 'constant'):
                self.constToStack(index)
            else:
                self.regToStack(segment, index)

            self.increaseStackPointer()

        elif (command == 'pop'):

            self.decreaseStackPointer()
            self.stackToReg(segment, index)


    # Stack Operator Commands
    def unaryOp(self, comp):
        """Pop one argument off the stack, perform comp.
        Properly manages stack pointer."""
        self.decreaseStackPointer()
        self.stackToDest('D')
        self.cCommand('D', comp)
        self.compToStack('D')
        self.increaseStackPointer()

    def binaryOp(self, comp):
        """Pops two arguments off the stack, perform comp.
        Properly manages stack pointer."""
        self.decreaseStackPointer()
        self.stackToDest('D')
        self.decreaseStackPointer()
        self.stackToDest('A')
        self.cCommand('D', comp)
        self.compToStack('D')
        self.increaseStackPointer()

    def logicalOp(self, jump):
        """Pops two arguments off the stack, perform comp.
        Properly manages stack pointer.
        Returns -1 for true, 0 for false."""
        # Create new label for branching
        # Note, this does not write it to asm
        trueLabel = self.newLabel()

        self.decreaseStackPointer()
        self.stackToDest('D')
        self.decreaseStackPointer()
        self.stackToDest('A')
        self.cCommand('D', 'A-D')
        self.compToStack('-1')
        self.aCommand(trueLabel)
        self.cCommand(None, 'D', jump)
        self.compToStack('0')
        self.lCommand(trueLabel)
        self.increaseStackPointer()


    # Register manipulators
    def registerAddress(self, segment, index):
        """Read the address of the register (segment index) into A and D."""
        segments = {'pointer': 3, 'temp': 5, 'local': 'LCL', 'argument': 'ARG',
                'this': 'THIS', 'that': 'THAT', 'static': self.staticLabel(index) }

        self.aCommand(index)
        self.cCommand('D', 'A')
        self.aCommand(segments[segment])
        if (segment in ['local', 'argument', 'this', 'that']):
            self.cCommand('A', 'M')
        self.cCommand('AD', 'D+A')


    # Write to stack commands
    def constToStack(self, const):
        """Place value at address to stack."""
        self.aCommand(const)
        self.cCommand('D', 'A')
        self.compToStack('D')

    def compToStack(self, comp):
        """Place the computation into the top of stack."""
        self.loadSP()
        self.cCommand('M', comp)

    def regToStack(self, segment, index):
        """Place the value of the register on the stack."""
        self.registerAddress(segment, index)
        self.cCommand('D', 'M') # compToStack overwrites A, so move to D first
        self.compToStack('D')


    # Read from stack commands
    def stackToDest(self, dest):
        """Place the value in the stack in the dest."""
        self.loadSP()
        self.cCommand(dest, 'M')

    def stackToReg(self, segment, index):
        """Place the value in the stack into the appropriate register."""
        self.registerAddress(segment, index)
        self.aCommand('R13')
        self.cCommand('M', 'D')
        self.stackToDest('D')
        self.aCommand('R13')
        self.cCommand('A', 'M')
        self.cCommand('M', 'D')


    # Stack pointer manipulators
    def increaseStackPointer(self):
        """Increase the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M+1')

    def decreaseStackPointer(self):
        """Decrease the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M-1')

    def loadSP(self):
        self.aCommand('SP')
        self.cCommand('A', 'M')


    # Command Writers
    def cCommand(self, dest, comp, jump = None):
        """Write out a C command in Hack assembly."""
        if (dest != None):
            self.outfile.write(dest + '=')
        self.outfile.write(comp)
        if (jump != None):
            self.outfile.write(';' + jump)
        self.outfile.write('\n')

    def aCommand(self, addr):
        """Write out an A command in Hack assemply."""
        self.outfile.write('@' + str(addr) + '\n')

    def lCommand(self, label):
        """Creates a new (label) for the assembler."""
        self.outfile.write('('+label+')\n')



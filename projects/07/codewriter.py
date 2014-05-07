# Current temporary stage one implementation of the VM Code Generator
#
# Stack Arithmetic, Logical Commands, push contstant x

import os
from parser import *

class CodeWriter:

    def __init__(self, outfile):
        """Opens the file output file/stream and gets
        ready to write into it."""

        isDirectory = outfile[-3:] != '.vm'

        self.outfile = open(outfile[:-3] + '.asm', 'w')

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

        while(p.hasMoreCommands()):
            p.advance()
            self.dispatchWriter(p.commandType(), p.currentCommand)


    def dispatchWriter(self, commandType, command):
        """Dispatches the write for the given command type."""

        if (commandType == 'C_ARITHMETIC'):
            self.writeArithmetic(command[0])
        elif (commandType == 'C_POP' or commandType == 'C_PUSH'):
            self.writePushPop(command[0], command[1], command[2])
        else:
            pass


    def writeArithmetic(self, command):
        """Writes the assembly code that is the given translation
        of the command given."""
        print command
        if (command == 'add'):
            self.binaryOp('D+A')
        elif (command == 'sub'):
            self.binaryOp('D-A')
        elif (command == 'neg'):
            self.unaryOp('-D')
        elif (command == 'eq'):
            # Uses Jump
            pass
        elif (command == 'gt'):
            # Uses Jump
            pass
        elif (command == 'lt'):
            # Uses Jump
            pass
        elif (command == 'and'):
            self.binaryOp('D&A')
        elif (command == 'or'):
            self.binaryOp('D|A')
        elif (command == 'not'):
            self.unaryOp('!D')

    def writePushPop(self, command, segment, index):
        """Writes the assembly code that is the translation of the
        given command, where command is either C_PUSH or C_POP."""
        if (command == 'push'):
            if (segment == 'constant'):
                # @ + index
                self.constToStack(index)
                self.increaseStackPointer()
        else:
            # push
            pass

        print command + ' ' + segment + ' ' + index

    def unaryOp(self, comp):
        """Pop one argument off the stack, perform comp.
        Properly manages stack pointer."""
        self.decreaseStackPointer()
        self.stackToDest('D')
        self.cCommand('D', comp)
        self.compToStack(comp)
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

    def increaseStackPointer(self):
        """Increase the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M+1')

    def decreaseStackPointer(self):
        """Decrease the stack pointer."""
        self.aCommand('SP')
        self.cCommand('M', 'M-1')

    def constToStack(self, const):
        """Place value at address to stack."""
        self.aCommand(const)
        self.cCommand('D', 'A')
        self.compToStack('D')

    def compToStack(self, comp):
        """Place the computation into the top of stack."""
        self.aCommand('SP')
        self.cCommand('M', comp)

    def stackToDest(self, dest):
        """Place the value in the stack in the dest."""
        self.aCommand('SP')
        self.cCommand(dest, 'M')

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
        self.outfile.write('@' + addr + '\n')


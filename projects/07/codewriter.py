# Current temporary stage one implementation of the VM Code Generator
#
# Stack Arithmetic, Logical Commands, push contstant x

class CodeWriter:

    def __init__(self, outfile):
        """Opens the file output file/stream and gets
        ready to write into it."""
        pass

    def setFileName(self, fileName):
        """Informs the code writer that the translations of
        a new VM file has started."""
        pass

    def writeArithmetic(self, command):
        """Writes the assembly code that is the given translation
        of the command given."""
        pass

    def writePushPop(self, command, segment, index):
        """Writes the assembly code that is the translation of the
        given command, where command is either C_PUSH or C_POP."""
        pass

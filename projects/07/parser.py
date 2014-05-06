# Current temporary stage one implementation of the VM parser
#
# Stack Arithmetic, Logical Commands, push contstant x


class parser:

    def __init__(self, infile):
        """Opens the input file/stream and gets ready to parse it."""
        pass

    def hasMoreCommands():
        """Are there more commands in the input?"""
        pass

    def advance():
        """Reads the next command from the input and makes it
        the current command. Should be called only if hasMoreCommands()
        is true. Initially there is no current command"""
        pass

    def commandType():
        """Returns the type of the current VM command.
        C_ARITHMETIC is returned for all the artihmetic commands."""
        pass

    def arg1():
        """Returns the first argument of the current command.
        In the case of C_ARITHMETIC the command itself (add,
        sub, etc.) is returned. Should not be called if the
        current command is C_RETURN."""
        pass

    def arg2():
        """Returns the second argument of the current command.
        Should be called only if the current command is
        C_PUSH, C_POP, C_FUNCTION, OR C_CALL."""
        pass

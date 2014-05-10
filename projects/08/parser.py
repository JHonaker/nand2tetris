# Current temporary stage one implementation of the VM parser
#
# Stack Arithmetic, Logical Commands, push contstant x

class parser:

    def __init__(self, infile):
        """Opens the input file/stream and gets ready to parse it."""

        # Open the file and read the raw commands
        f = open(infile)
        self.commands = f.readlines()
        f.close()

        # Strip comments and whitespace from the end of lines
        self.commands = [com.split('//')[0] for com in self.commands]
        self.commands = [com.strip() for com in self.commands]

        # Remove blank lines and comment-only lines from the command list
        self.commands = self._trimLines()

        # Initialize the first command to -1 (Initially blank command)
        self.cmdIndex = -1
        self.currentCommand = None

    def _trimLines(self):
        """Removes blank lines and comment (//) only lines from self.commands"""

        tempCommands = []
        for i in range(0, len(self.commands)):
            if self.commands[i] != '' and self.commands[i][0:2] != '//':
                tempCommands.append(self.commands[i])
        return tempCommands


    def hasMoreCommands(self):
        """Are there more commands in the input?"""

        return self.cmdIndex < len(self.commands) - 1

    def advance(self):
        """Reads the next command from the input and makes it
        the current command. Should be called only if hasMoreCommands(self)
        is true. Initially there is no current command"""

        if (self.hasMoreCommands() == True):
            self.cmdIndex += 1
            self.currentCommand = self.commands[self.cmdIndex].split(' ')

    def commandType(self):
        """Returns the type of the current VM command.
        C_ARITHMETIC is returned for all the artihmetic commands."""

        C_ARITHMETIC = [
                'add', 'sub', 'neg', 'eq', 'gt',
                'lt', 'and', 'or', 'not'
                ]

        command = self.currentCommand


        if (command[0] in C_ARITHMETIC):
            return 'C_ARITHMETIC'

        elif (command[0] == 'push'):
            return 'C_PUSH'

        elif (command[0] == 'pop'):
            return 'C_POP'

        elif (command[0] == 'goto'):
            return 'C_GOTO'

        elif (command[0] == 'if-goto'):
            return 'C_IF'

        elif (command[0] == 'function'):
            return 'C_FUNCTION'

        elif (command[0] == 'return'):
            return 'C_RETURN'

        elif (command[0] == 'call'):
            return 'C_CALL'


    def arg1(self):
        """Returns the first argument of the current command.
        In the case of C_ARITHMETIC the command itself (add,
        sub, etc.) is returned. Should not be called if the
        current command is C_RETURN."""

        if (self.commandType() == 'C_RETURN'):
            return None

        elif (self.commandType() == 'C_ARITHMETIC'):
            return self.currentCommand[0]

        else:
            return self.currentCommand[1]

    def arg2(self):
        """Returns the second argument of the current command.
        Should be called only if the current command is
        C_PUSH, C_POP, C_FUNCTION, OR C_CALL."""

        if (self.commandType() in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']):
            return self.currentCommand[2]
        else:
            return None
